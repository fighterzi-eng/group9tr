#!/usr/bin/env python3

import rospy
import json
import os
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from std_msgs.msg import String

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Global variable to store orders
orders = []
order_counter = 1

@app.route('/status', methods=['GET'])
def status():
    """Endpoint to check if ROS node is running"""
    return jsonify({"status": "active", "ros_time": rospy.get_time()})

@app.route('/order', methods=['POST'])
def receive_order():
    """Endpoint to receive orders from the web interface"""
    global order_counter
    
    try:
        order_data = request.get_json()
        
        # Add order ID and timestamp
        order_data['order_id'] = order_counter
        order_data['ros_received_time'] = rospy.get_time()
        
        # Save order to file
        save_order(order_data)
        
        # Publish order to ROS topic
        publish_order(order_data)
        
        # Increment order counter
        order_counter += 1
        
        return jsonify({
            "status": "success", 
            "order_id": order_data['order_id'],
            "message": "Order received and processed"
        })
    
    except Exception as e:
        rospy.logerr(f"Error processing order: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

def save_order(order_data):
    """Save order to a JSON file"""
    try:
        # Create orders directory if it doesn't exist
        orders_dir = os.path.join(os.path.expanduser("~"), "decepticons_orders")
        if not os.path.exists(orders_dir):
            os.makedirs(orders_dir)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"order_{order_data['order_id']}_{timestamp}.json"
        filepath = os.path.join(orders_dir, filename)
        
        # Write order to file
        with open(filepath, 'w') as f:
            json.dump(order_data, f, indent=2)
        
        rospy.loginfo(f"Order saved to {filepath}")
    
    except Exception as e:
        rospy.logerr(f"Error saving order: {str(e)}")

def publish_order(order_data):
    """Publish order to ROS topic"""
    try:
        # Create a publisher
        pub = rospy.Publisher('/decepticons_orders', String, queue_size=10)
        
        # Convert order to JSON string
        order_json = json.dumps(order_data)
        
        # Create and publish message
        msg = String()
        msg.data = order_json
        pub.publish(msg)
        
        rospy.loginfo(f"Order published to ROS topic: {order_data['order_id']}")
    
    except Exception as e:
        rospy.logerr(f"Error publishing order to ROS: {str(e)}")

def ros_node():
    """Initialize ROS node"""
    rospy.init_node('decepticons_diner', anonymous=True)
    rospy.loginfo("Decepticons Diner ROS node started")
    
    # Run Flask app in a separate thread
    from threading import Thread
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Keep ROS node running
    rospy.spin()

def run_flask():
    """Run Flask web server"""
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    try:
        ros_node()
    except rospy.ROSInterruptException:
        pass