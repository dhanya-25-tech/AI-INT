import requests

# Test candidate URLs for Kitchen, Living Room, Bathroom, Bedroom
TEST_URLS = {
    "kitchen": [
        "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=800&auto=format&fit=crop", # Kitchen 1
        "https://images.unsplash.com/photo-1507089947368-19c1da9775ae?w=800&auto=format&fit=crop", # Kitchen 2
        "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800&auto=format&fit=crop", # Kitchen 3
        "https://images.unsplash.com/photo-1528698827591-e19ccd7bc23d?w=800&auto=format&fit=crop", # Kitchen 4
        "https://images.unsplash.com/photo-1565538810643-b5bdb714032a?w=800&auto=format&fit=crop", # Kitchen 5
        "https://images.unsplash.com/photo-1556909212-d5b604d0c90d?w=800&auto=format&fit=crop", # Luxury Kitchen 1
        "https://images.unsplash.com/photo-1556912172-45b7abe8b7e1?w=800&auto=format&fit=crop", # Luxury Kitchen 2
        "https://images.unsplash.com/photo-1556912167-f556f1f39fdf?w=800&auto=format&fit=crop", # Luxury Kitchen 3
        "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=800&auto=format&fit=crop", # Luxury Kitchen 4
        "https://images.unsplash.com/photo-1507089947368-19c1da9775ae?w=800&auto=format&fit=crop"  # Luxury Kitchen 5
    ],
    "livingroom": [
        "https://images.unsplash.com/photo-1583847268964-b28dc8f51f92?w=800&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1554995207-c18c203602cb?w=800&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1567016432779-094069958ea5?w=800&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?w=800&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?w=800&auto=format&fit=crop"
    ],
    "bathroom": [
        "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=800&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1507652313519-d4e9174996dd?w=800&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1620626011761-996317b8d101?w=800&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1552321554-5fefe8c9ef14?w=800&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1604014237800-1c9102c219da?w=800&auto=format&fit=crop"
    ],
    "bedroom": [
        "https://images.unsplash.com/photo-1616594039964-ae9021a400a0?w=800&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?w=800&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=800&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1598928506311-c55ded91a20c?w=800&auto=format&fit=crop"
    ]
}

def check_urls():
    for cat, urls in TEST_URLS.items():
        print(f"\nChecking {cat.upper()} URLs:")
        for idx, url in enumerate(urls):
            try:
                res = requests.get(url, timeout=5)
                print(f"  [{idx+1}] {res.status_code} | Bytes: {len(res.content)} | URL: {url[:60]}...")
            except Exception as e:
                print(f"  [{idx+1}] FAILED: {e}")

if __name__ == "__main__":
    check_urls()
