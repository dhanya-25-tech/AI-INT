import requests

# Test dictionary mapping for 4 rooms x 3 styles (60 unique photo URLs)
ALL_ROOM_PHOTOS = {
    "bedroom": {
        "simple": [
            "https://images.unsplash.com/photo-1616594039964-ae9021a400a0?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1598928506311-c55ded91a20c?w=800&auto=format&fit=crop"
        ],
        "luxurious": [
            "https://images.unsplash.com/photo-1590490360182-c33d57733427?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1617325247661-675ab4b64ae2?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1566665797739-1674de7a421a?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1618773928121-c32242e63f39?w=800&auto=format&fit=crop"
        ],
        "rich": [
            "https://images.unsplash.com/photo-1616046229478-9901c5536a45?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1560185127-6ed189bf02f4?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1512918728675-ed5a9ecdebfd?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=800&auto=format&fit=crop"
        ]
    },
    "kitchen": {
        "simple": [
            "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1507089947368-19c1da9775ae?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1528698827591-e19ccd7bc23d?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1565538810643-b5bdb714032a?w=800&auto=format&fit=crop"
        ],
        "luxurious": [
            "https://images.unsplash.com/photo-1556909212-d5b604d0c90d?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1556912172-45b7abe8b7e1?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1556912167-f556f1f39fdf?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=800&auto=format&fit=crop"
        ],
        "rich": [
            "https://images.unsplash.com/photo-1600585154526-990dced4db0d?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1600566752355-35792bedcfea?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1600585152220-90363fe7e115?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1600585154363-67eb9e2e2099?w=800&auto=format&fit=crop"
        ]
    },
    "bathroom": {
        "simple": [
            "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1507652313519-d4e9174996dd?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1620626011761-996317b8d101?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1552321554-5fefe8c9ef14?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1604014237800-1c9102c219da?w=800&auto=format&fit=crop"
        ],
        "luxurious": [
            "https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1600573472591-ee6b68d14c68?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1600566753376-12c8ab7fb75b?w=800&auto=format&fit=crop"
        ],
        "rich": [
            "https://images.unsplash.com/photo-1600585154526-990dced4db0d?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1600566752355-35792bedcfea?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1600585152220-90363fe7e115?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1600585154363-67eb9e2e2099?w=800&auto=format&fit=crop"
        ]
    },
    "livingroom": {
        "simple": [
            "https://images.unsplash.com/photo-1583847268964-b28dc8f51f92?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1554995207-c18c203602cb?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1567016432779-094069958ea5?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?w=800&auto=format&fit=crop"
        ],
        "luxurious": [
            "https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=800&auto=format&fit=crop"
        ],
        "rich": [
            "https://images.unsplash.com/photo-1616046229478-9901c5536a45?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1560185127-6ed189bf02f4?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1512918728675-ed5a9ecdebfd?w=800&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=800&auto=format&fit=crop"
        ]
    }
}

def verify_style_uniqueness():
    for room, styles in ALL_ROOM_PHOTOS.items():
        simple_set = set(styles["simple"])
        luxurious_set = set(styles["luxurious"])
        rich_set = set(styles["rich"])

        print(f"\nChecking style uniqueness for {room.upper()}:")
        print(f"  Simple vs Luxurious overlap: {len(simple_set.intersection(luxurious_set))}")
        print(f"  Simple vs Rich overlap: {len(simple_set.intersection(rich_set))}")
        print(f"  Luxurious vs Rich overlap: {len(luxurious_set.intersection(rich_set))}")

if __name__ == "__main__":
    verify_style_uniqueness()
