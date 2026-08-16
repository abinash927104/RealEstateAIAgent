import asyncio
import os
import shutil

from sqlalchemy import select, func, text
from app.db.session import async_session_factory, init_db
from app.models.property import Property, PropertyType, PropertyStatus
from app.services.vector_service import VectorService

INDIAN_PROPERTIES = [
    {
        "title": "Luxury Sea-Facing Apartment in Bandra",
        "description": "Stunning 4BHK apartment with panoramic views of the Arabian Sea. Features Italian marble flooring, a modular kitchen, and an expansive balcony. Premium amenities include a rooftop infinity pool and state-of-the-art gym.",
        "price": 45000000,
        "property_type": PropertyType.APARTMENT,
        "bedrooms": 4,
        "bathrooms": 4,
        "area_sqft": 2500,
        "address": "Carter Road, Bandra West",
        "city": "Mumbai",
        "state": "MH",
        "zip_code": "400050",
        "latitude": 19.0660,
        "longitude": 72.8258,
        "features": {"sea_view": True, "gym": True, "swimming_pool": True, "balcony": True, "modular_kitchen": True},
        "images": ["https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800"],
        "year_built": 2021,
        "parking_spaces": 2,
        "hoa_monthly": 15000,
    },
    {
        "title": "IT Corridor Premium Villa",
        "description": "Spacious 4BHK independent villa in a gated community in Whitefield, close to major tech parks. Features a private garden, home theater room, and modern aesthetics.",
        "price": 32000000,
        "property_type": PropertyType.HOUSE,
        "bedrooms": 4,
        "bathrooms": 4,
        "area_sqft": 3200,
        "address": "Palm Meadows, Whitefield",
        "city": "Bengaluru",
        "state": "KA",
        "zip_code": "560066",
        "latitude": 12.9698,
        "longitude": 77.7499,
        "features": {"private_garden": True, "gated_community": True, "clubhouse": True, "home_theater": True},
        "images": ["https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800"],
        "year_built": 2018,
        "lot_size_sqft": 4000,
        "parking_spaces": 2,
    },
    {
        "title": "Spacious 3BHK Flat in Andheri West",
        "description": "Well-lit and ventilated 3BHK apartment in the heart of Andheri West. Walking distance to the metro station and major shopping malls. Perfect for families.",
        "price": 27500000,
        "property_type": PropertyType.APARTMENT,
        "bedrooms": 3,
        "bathrooms": 3,
        "area_sqft": 1500,
        "address": "Lokhandwala Complex",
        "city": "Mumbai",
        "state": "MH",
        "zip_code": "400053",
        "latitude": 19.1415,
        "longitude": 72.8266,
        "features": {"near_metro": True, "security": True, "lift": True, "park": True},
        "images": ["https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800"],
        "year_built": 2015,
        "parking_spaces": 1,
        "hoa_monthly": 8000,
    },
    {
        "title": "Affordable 2BHK Starter Home",
        "description": "Brand new 2BHK apartment in Hinjewadi Phase 1, ideal for IT professionals. Project offers excellent amenities including a coworking space, gym, and swimming pool.",
        "price": 8500000,
        "property_type": PropertyType.APARTMENT,
        "bedrooms": 2,
        "bathrooms": 2,
        "area_sqft": 950,
        "address": "Hinjewadi Phase 1",
        "city": "Pune",
        "state": "MH",
        "zip_code": "411057",
        "latitude": 18.5913,
        "longitude": 73.7389,
        "features": {"coworking_space": True, "swimming_pool": True, "gym": True, "near_it_park": True},
        "images": ["https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=800"],
        "year_built": 2023,
        "parking_spaces": 1,
        "hoa_monthly": 4000,
    },
    {
        "title": "Modern Townhouse in OMR",
        "description": "Contemporary 3BHK townhouse located on the Old Mahabalipuram Road. Features an open-plan living area, a private terrace, and access to a massive clubhouse.",
        "price": 15000000,
        "property_type": PropertyType.TOWNHOUSE,
        "bedrooms": 3,
        "bathrooms": 3,
        "area_sqft": 1800,
        "address": "OMR IT Expressway, Sholinganallur",
        "city": "Chennai",
        "state": "TN",
        "zip_code": "600119",
        "latitude": 12.9010,
        "longitude": 80.2279,
        "features": {"private_terrace": True, "clubhouse": True, "power_backup": True},
        "images": ["https://images.unsplash.com/photo-1580587771525-78b9dba3b914?w=800"],
        "year_built": 2020,
        "parking_spaces": 2,
        "hoa_monthly": 5000,
    },
    {
        "title": "Premium Builder Floor in South Ex",
        "description": "Luxurious 4BHK builder floor in South Extension Part 2. Comes with high-end fittings, central air conditioning, and exclusive roof rights. Located in a prime residential neighborhood.",
        "price": 50000000,
        "property_type": PropertyType.APARTMENT,
        "bedrooms": 4,
        "bathrooms": 4,
        "area_sqft": 2800,
        "address": "South Extension Part 2",
        "city": "New Delhi",
        "state": "DL",
        "zip_code": "110049",
        "latitude": 28.5677,
        "longitude": 77.2185,
        "features": {"central_ac": True, "roof_rights": True, "premium_fittings": True, "prime_location": True},
        "images": ["https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800"],
        "year_built": 2022,
        "parking_spaces": 2,
    },
    {
        "title": "Luxury 4BHK Penthouse with Private Pool",
        "description": "Exquisite 4BHK penthouse in HITEC City featuring a private plunge pool, expansive terrace, and smart home automation. Offers uninterrupted skyline views.",
        "price": 41000000,
        "property_type": PropertyType.APARTMENT,
        "bedrooms": 4,
        "bathrooms": 5,
        "area_sqft": 4000,
        "address": "HITEC City Main Road",
        "city": "Hyderabad",
        "state": "TS",
        "zip_code": "500081",
        "latitude": 17.4435,
        "longitude": 78.3772,
        "features": {"private_pool": True, "smart_home": True, "terrace": True, "skyline_view": True},
        "images": ["https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800"],
        "year_built": 2021,
        "parking_spaces": 3,
        "hoa_monthly": 12000,
    },
    {
        "title": "Smart 2BHK in Electronic City",
        "description": "Budget-friendly 2BHK flat close to Infosys campus. Excellent for rental yield. Complex includes a badminton court, jogging track, and 24/7 security.",
        "price": 6500000,
        "property_type": PropertyType.APARTMENT,
        "bedrooms": 2,
        "bathrooms": 2,
        "area_sqft": 1050,
        "address": "Electronic City Phase 1",
        "city": "Bengaluru",
        "state": "KA",
        "zip_code": "560100",
        "latitude": 12.8452,
        "longitude": 77.6602,
        "features": {"jogging_track": True, "security": True, "badminton_court": True},
        "images": ["https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800"],
        "year_built": 2019,
        "parking_spaces": 1,
        "hoa_monthly": 3000,
    },
    {
        "title": "Ultra-Luxury Condo on Golf Course Road",
        "description": "Lavish 4BHK condominium with direct views of the golf course. Features VRV air conditioning, imported marble, and access to a 5-star club.",
        "price": 65000000,
        "property_type": PropertyType.CONDO,
        "bedrooms": 4,
        "bathrooms": 4,
        "area_sqft": 3500,
        "address": "Golf Course Road, Sector 54",
        "city": "Gurgaon",
        "state": "HR",
        "zip_code": "122011",
        "latitude": 28.4410,
        "longitude": 77.1030,
        "features": {"golf_course_view": True, "vrv_ac": True, "luxury_club": True, "concierge": True},
        "images": ["https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800"],
        "year_built": 2020,
        "parking_spaces": 2,
        "hoa_monthly": 18000,
    },
    {
        "title": "Spacious 3BHK on Noida Expressway",
        "description": "Premium 3BHK apartment in Sector 150, Noida. Low density project with 80% green area. Includes modular kitchen, wardrobes, and golf-themed landscaping.",
        "price": 12500000,
        "property_type": PropertyType.APARTMENT,
        "bedrooms": 3,
        "bathrooms": 3,
        "area_sqft": 1850,
        "address": "Sector 150",
        "city": "Noida",
        "state": "UP",
        "zip_code": "201310",
        "latitude": 28.4310,
        "longitude": 77.4580,
        "features": {"green_area": True, "modular_kitchen": True, "golf_theme": True},
        "images": ["https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=800"],
        "year_built": 2022,
        "parking_spaces": 1,
        "hoa_monthly": 6000,
    },
    {
        "title": "Independent House in Jayanagar",
        "description": "Classic 4BHK independent house in the prestigious Jayanagar 4th Block. Features a traditional layout, large courtyard, and mature trees on the property.",
        "price": 48000000,
        "property_type": PropertyType.HOUSE,
        "bedrooms": 4,
        "bathrooms": 3,
        "area_sqft": 3000,
        "address": "Jayanagar 4th Block",
        "city": "Bengaluru",
        "state": "KA",
        "zip_code": "560011",
        "latitude": 12.9299,
        "longitude": 77.5834,
        "features": {"courtyard": True, "mature_trees": True, "traditional_layout": True},
        "images": ["https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=800"],
        "year_built": 1995,
        "lot_size_sqft": 4000,
        "parking_spaces": 2,
    },
    {
        "title": "Modern 1BHK Studio in Koregaon Park",
        "description": "Chic 1BHK studio apartment in Koregaon Park, surrounded by cafes and boutiques. Ideal for young professionals or as an Airbnb investment.",
        "price": 7500000,
        "property_type": PropertyType.APARTMENT,
        "bedrooms": 1,
        "bathrooms": 1,
        "area_sqft": 650,
        "address": "Koregaon Park",
        "city": "Pune",
        "state": "MH",
        "zip_code": "411001",
        "latitude": 18.5362,
        "longitude": 73.8939,
        "features": {"fully_furnished": True, "prime_location": True, "near_cafes": True},
        "images": ["https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800"],
        "year_built": 2017,
        "parking_spaces": 1,
        "hoa_monthly": 2500,
    }
]


from app.db.seed import KNOWLEDGE_BASE

async def reseed_database():
    """Clear existing DB and seed with Indian properties."""
    print("🧹 Clearing database...")
    await init_db()

    async with async_session_factory() as db:
        # Delete existing data (Cascade deletes favorites too)
        await db.execute(text("TRUNCATE TABLE properties CASCADE"))
        await db.commit()
        print("  ✅ Properties table truncated.")

        print("🌱 Seeding Indian properties...")
        for prop_data in INDIAN_PROPERTIES:
            prop = Property(**prop_data)
            db.add(prop)

        await db.commit()
        print(f"  ✅ Inserted {len(INDIAN_PROPERTIES)} properties")

    # Seed vector store
    print("  Re-indexing properties in ChromaDB...")
    
    # We will just instantiate VectorService which recreates the collection if we deleted the data dir
    vector_service = VectorService()

    async with async_session_factory() as db:
        result = await db.execute(select(Property))
        properties = result.scalars().all()

        for prop in properties:
            await vector_service.add_property(
                str(prop.id),
                {
                    "title": prop.title,
                    "description": prop.description,
                    "price": float(prop.price),
                    "property_type": prop.property_type.value,
                    "bedrooms": prop.bedrooms,
                    "bathrooms": prop.bathrooms,
                    "area_sqft": prop.area_sqft,
                    "city": prop.city,
                    "state": prop.state,
                    "features": prop.features,
                    "status": prop.status.value,
                },
            )

    print(f"  ✅ Indexed {len(properties)} properties in ChromaDB")

    # Seed knowledge base
    print("  Loading knowledge base...")
    for entry in KNOWLEDGE_BASE:
        await vector_service.add_knowledge(
            entry["id"], entry["content"], entry["metadata"]
        )

    print(f"  ✅ Loaded {len(KNOWLEDGE_BASE)} knowledge base entries")
    print("🎉 Indian Reseeding complete!")


if __name__ == "__main__":
    # Force delete chromadb folder to ensure clean state
    if os.path.exists("./data/chroma"):
        shutil.rmtree("./data/chroma")
        print("🗑️  Deleted existing ChromaDB data.")
        
    asyncio.run(reseed_database())
