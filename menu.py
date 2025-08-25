import tkinter as tk
from tkinter import ttk, messagebox
import random

class CyberTronRestaurant:
    def __init__(self, root):
        self.root = root
        self.root.title("CyberTron Restaurant - Interactive Menu")
        self.root.geometry("1000x700")
        self.root.configure(bg="#0a0a1a")

        self.cart = []

        self.menu_items = {
            "Main Course": {
                "Pizza": {
                    "description": "Delicious pizza with tomato sauce and mozzarella", 
                    "sizes": {"S": 185, "M": 220, "L": 260},
                    "addons": {"Extra Cheese": 30, "Pepperoni": 75, "Mushrooms": 80}
                },
                "Burger": {
                    "description": "Juicy beef patty with fresh vegetables", 
                    "sizes": {"S": 165, "M": 190, "L": 220},
                    "addons": {"Extra Cheese": 30, "Bacon": 50, "Mozzarella Sticks": 30}
                }
            },
            "Snacks": {
                "Mozzarella Sticks": {
                    "description": "Crispy fried mozzarella with marinara sauce", 
                    "sizes": {"S": 35, "M": 45, "L": 55},
                    "addons": {"Extra Sauce": 25, "Parmesan": 40}
                },
                "Onion Rings": {
                    "description": "Golden fried onion rings with dipping sauce", 
                    "sizes": {"S": 30, "M": 40, "L": 50},
                    "addons": {"Extra Sauce": 25, "Spicy Seasoning": 30}
                }
            },
            "Dessert": {
                "Cup Cake": {
                    "description": "Sweet vanilla cupcake with buttercream frosting", 
                    "sizes": {"S": 45, "M": 55, "L": 65},
                    "addons": {"Chocolate": 50, "Sprinkles": 20}
                },
                "Cheese Cake": {
                    "description": "Creamy New York style cheesecake", 
                    "sizes": {"S": 55, "M": 65, "L": 75},
                    "addons": {"Berry Compote": 18, "Whipped Cream": 40}
                }
            },
            "Drinks": {
                "Pepsi": {
                    "description": "Refreshing cola drink", 
                    "sizes": {"S": 15, "M": 20, "L": 25},
                    "addons": {"Ice": 0, "Lemon": 5}
                },
                "Water": {
                    "description": "Pure bottled water", 
                    "sizes": {"S": 10, "M": 15, "L": 20},
                    "addons": {"Ice": 0, "Lemon": 5}
                }
            }
        }
        
        self.create_widgets()
        
    def create_widgets(self):
        style = ttk.Style()
        style.configure("TNotebook", background="#0a0a1a", borderwidth=0)
        style.configure("TNotebook.Tab", background="#737377", foreground="cyan", padding=[20, 10], font=('Arial', 14, 'bold'))
        style.map("TNotebook.Tab", background=[("selected", "#4a4a8a")])
        
        self.notebook = ttk.Notebook(self.root, style="TNotebook")
        self.notebook.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.frames = {}
        for category in self.menu_items.keys():
            self.frames[category] = tk.Frame(self.notebook, bg="#0a0a1a")
            self.notebook.add(self.frames[category], text=category)
            self.add_items_to_category(category, self.frames[category])

        self.create_cart_frame()
        
    def add_items_to_category(self, category, frame):
        row, col = 0, 0
        for item, details in self.menu_items[category].items():
            item_frame = tk.Frame(frame, bg="#64646d", relief="raised", bd=2)
            item_frame.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

            name_label = tk.Label(item_frame, text=item, font=("Arial", 14, "bold"), 
                                 fg="cyan", bg="#64646d")
            name_label.pack(pady=(10, 5))

            desc_label = tk.Label(item_frame, text=details["description"], 
                                 font=("Arial", 10), fg="white", bg="#64646d", wraplength=200)
            desc_label.pack(pady=5)

            size_frame = tk.Frame(item_frame, bg="#64646d")
            size_frame.pack(pady=5)
            
            size_label = tk.Label(size_frame, text="Size:", font=("Arial", 10, "bold"), 
                                 fg="white", bg="#64646d")
            size_label.pack(side="left")
            
            size_var = tk.StringVar(value="M") 
            
            for size, price in details["sizes"].items():
                size_btn = tk.Radiobutton(size_frame, text=f"{size} ({price} EGP)", 
                                         variable=size_var, value=size,
                                         fg="white", bg="#64646d", selectcolor="#4a4a8a",
                                         font=("Arial", 9))
                size_btn.pack(side="left", padx=5)
 
            addon_frame = tk.Frame(item_frame, bg="#64646d")
            addon_frame.pack(pady=5)
            
            addon_vars = {}
            for addon, addon_price in details["addons"].items():
                var = tk.BooleanVar()
                chk = tk.Checkbutton(addon_frame, text=f"{addon} (+{addon_price} EGP)", 
                                    variable=var, fg="white", bg="#64646d", 
                                    selectcolor="#4a4a8a", font=("Arial", 9))
                chk.pack(anchor="w")
                addon_vars[addon] = (var, addon_price)

            add_btn = tk.Button(item_frame, text="Add to Cart", 
                               command=lambda i=item, s=size_var, a=addon_vars, c=category: 
                               self.add_to_cart(i, s, a, c),
                               bg="#00cc66", fg="white", font=("Arial", 10, "bold"))
            add_btn.pack(pady=10)
            
            col += 1
            if col > 1:
                col = 0
                row += 1
        
        for i in range(2):
            frame.columnconfigure(i, weight=1)
        for i in range(row + 1):
            frame.rowconfigure(i, weight=1)
    
    def create_cart_frame(self):

        self.cart_frame = tk.Frame(self.root, bg="#0a0a1a")
        self.cart_frame.pack(fill="x", padx=10, pady=10)

        cart_title = tk.Label(self.cart_frame, text="Your Cart", font=("Arial", 16, "bold"), 
                             fg="cyan", bg="#0a0a1a")
        cart_title.pack(anchor="w")

        self.cart_items_frame = tk.Frame(self.cart_frame, bg="#0a0a1a")
        self.cart_items_frame.pack(fill="x", pady=10)

        self.delivery_var = tk.BooleanVar()
        delivery_chk = tk.Checkbutton(self.cart_frame, text="Home Delivery (+$10)", 
                                     variable=self.delivery_var, command=self.update_total,
                                     fg="white", bg="#0a0a1a", selectcolor="#4a4a8a", 
                                     font=("Arial", 12))
        delivery_chk.pack(anchor="w", pady=5)

        self.total_label = tk.Label(self.cart_frame, text="Total: 0 EGP", 
                                   font=("Arial", 14, "bold"), fg="yellow", bg="#0a0a1a")
        self.total_label.pack(anchor="w", pady=5)

        btn_frame = tk.Frame(self.cart_frame, bg="#0a0a1a")
        btn_frame.pack(fill="x", pady=10)

        confirm_btn = tk.Button(btn_frame, text="Confirm Order", command=self.confirm_order,
                               bg="#1eff00", fg="white", font=("Arial", 12, "bold"))
        confirm_btn.pack(side="left", padx=5)

        cancel_btn = tk.Button(btn_frame, text="Cancel Order", command=self.cancel_order,
                              bg="#ff6666", fg="white", font=("Arial", 12, "bold"))
        cancel_btn.pack(side="left", padx=5)
        
        reset_btn = tk.Button(btn_frame, text="Reset", command=self.reset_cart,
                             bg="#ffcc00", fg="black", font=("Arial", 12, "bold"))
        reset_btn.pack(side="left", padx=5)
    
    def add_to_cart(self, item, size_var, addons_vars, category):
        selected_size = size_var.get()
        base_price = self.menu_items[category][item]["sizes"][selected_size]

        addons = []
        addons_total = 0
        for addon, (var, price) in addons_vars.items():
            if var.get():
                addons.append(addon)
                addons_total += price

        total_price = base_price + addons_total
        self.cart.append({
            "item": item,
            "size": selected_size,
            "base_price": base_price,
            "addons": addons,
            "addons_total": addons_total,
            "total_price": total_price,
            "category": category
        })
        
        self.update_cart_display()
        messagebox.showinfo("Added to Cart", f"{item} ({selected_size}) has been added to your cart!")
    
    def update_cart_display(self):
        for widget in self.cart_items_frame.winfo_children():
            widget.destroy()
        
        if not self.cart:
            empty_label = tk.Label(self.cart_items_frame, text="Your cart is empty", 
                                  font=("Arial", 12), fg="white", bg="#0a0a1a")
            empty_label.pack(anchor="w")
            return

        for i, item in enumerate(self.cart):
            item_text = f"{item['item']} ({item['size']}) - {item['total_price']} EGP"
            if item['addons']:
                item_text += f" (with {', '.join(item['addons'])})"
            
            item_label = tk.Label(self.cart_items_frame, text=item_text, 
                                 font=("Arial", 10), fg="white", bg="#0a0a1a")
            item_label.pack(anchor="w")
        
        self.update_total()
    
    def update_total(self):
        total = sum(item['total_price'] for item in self.cart)
        if self.delivery_var.get():
            total += 10
        
        self.total_label.config(text=f"Total: {total} EGP")
    
    def confirm_order(self):
        if not self.cart:
            messagebox.showwarning("Empty Cart", "Your cart is empty. Please add items before confirming.")
            return
        
        total = sum(item['total_price'] for item in self.cart)
        if self.delivery_var.get():
            total += 10
            delivery_text = "with Delivery"
        else:
            delivery_text = "for Pickup"
        
        order_details = "\n".join([
            f"{item['item']} ({item['size']}) - {item['total_price']} EGP " + 
            (f"(with {', '.join(item['addons'])})" if item['addons'] else "")
            for item in self.cart
        ])
        
        confirm_msg = f"Confirm your order {delivery_text}?\n\n{order_details}\n\nTotal: {total} EGP"
        if messagebox.askyesno("Confirm Order", confirm_msg):
            order_number = random.randint(1000, 9999)
            messagebox.showinfo("Order Confirmed", 
                               f"Your order has been confirmed!\nOrder Number: #{order_number}\nEstimated waiting time: 20-30 minutes")
            self.reset_cart()
    
    def cancel_order(self):
        if not self.cart:
            return
            
        if messagebox.askyesno("Cancel Order", "Are you sure you want to cancel your order?"):
            self.reset_cart()
            messagebox.showinfo("Order Cancelled", "Your order has been cancelled.")
    
    def reset_cart(self):
        self.cart = []
        self.delivery_var.set(False)
        self.update_cart_display()
        self.update_total()

if __name__ == "__main__":
    root = tk.Tk()
    app = CyberTronRestaurant(root)
    root.mainloop()
