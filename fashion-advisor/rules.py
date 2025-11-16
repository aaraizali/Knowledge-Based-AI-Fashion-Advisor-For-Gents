# rules.py

rules = {
    "weather": {
        "hot": {
            "top": ["White Cotton Shirt", "Light Blue Dress Shirt", "Casual Linen Shirt", "Navy Polo Shirt"],
            "bottom": ["Khaki Chinos", "Dark Blue Jeans", "Casual Shorts"],
            "shoes": ["White Sneakers", "Brown Loafers", "Casual Slip-On Sneakers"],
            "reason": "Light and breathable fabrics keep you comfortable in hot weather."
        },
        "mild": {
            "top": ["Casual Chambray Shirt", "Grey Turtleneck Sweater", "Black Slim-Fit Sweater"],
            "bottom": ["Dark Blue Jeans", "Khaki Chinos", "Olive Chinos"],
            "shoes": ["White Sneakers", "Brown Loafers", "Chelsea Boots"],
            "reason": "Moderate fabrics and layers work well for mild weather."
        },
        "cold": {
            "top": ["Grey Turtleneck Sweater", "Black Slim-Fit Sweater", "Casual Chambray Shirt", "Navy Polo Shirt"],
            "bottom": ["Dark Blue Jeans", "Grey Dress Trousers", "Navy Dress Pants"],
            "shoes": ["Chelsea Boots", "Derby Shoes", "Black Oxford Shoes"],
            "reason": "Warm layers and sturdy shoes help in cold weather."
        }
    },
    "occasion": {
        "formal": {
            "addon": ["Blazer", "Tie", "Leather Belt"],
            "shoes": ["Black Oxford Shoes", "Brown Derby Shoes"],
            "reason": "Formal events require polished looks with matching accessories."
        },
        "casual": {
            "addon": ["Casual Jacket", "Watch"],
            "shoes": ["White Sneakers", "Casual Slip-On Sneakers"],
            "reason": "Casual outfits can be comfortable but stylish."
        },
        "party": {
            "addon": ["Leather Jacket", "Watch or Bracelet"],
            "shoes": ["Chelsea Boots", "Brown Loafers"],
            "reason": "Party outfits should be stylish and eye-catching."
        }
    },
    "body_type": {
        "athletic": {"fit": "Slim-fit clothing enhances your athletic body type."},
        "slim": {"fit": "You can layer slightly to add volume and style."},
        "heavy": {"fit": "Relaxed or straight-fit clothing provides comfort and balance."}
    },
    "style": {
        "Classic": {"pattern": "Classic patterns and neutral colors are timeless."},
        "Sporty": {"pattern": "Sporty styles with casual pieces and sneakers."},
        "Trendy": {"pattern": "Current fashion trends with modern cuts and combinations."}
    }
}
