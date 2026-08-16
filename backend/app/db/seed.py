"""
Seed script — populate the database with sample real estate properties.
Run with: python -m app.db.seed
"""

import asyncio
import random

from app.db.session import async_session_factory, init_db
from app.models.property import Property, PropertyType, PropertyStatus
from app.services.vector_service import VectorService
from app.utils.embeddings import create_property_document


SAMPLE_PROPERTIES = [
    {
        "title": "Modern Downtown Loft with City Views",
        "description": "Stunning open-concept loft in the heart of downtown. Floor-to-ceiling windows offer breathtaking city views. Recently renovated with high-end finishes, quartz countertops, and hardwood floors throughout.",
        "price": 485000,
        "property_type": PropertyType.APARTMENT,
        "bedrooms": 2,
        "bathrooms": 2,
        "area_sqft": 1200,
        "address": "456 Main Street, Unit 12A",
        "city": "Austin",
        "state": "TX",
        "zip_code": "78701",
        "latitude": 30.2672,
        "longitude": -97.7431,
        "features": {"hardwood_floors": True, "city_views": True, "gym": True, "parking": True, "concierge": True},
        "images": ["https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800"],
        "year_built": 2019,
        "parking_spaces": 1,
        "hoa_monthly": 350,
    },
    {
        "title": "Charming Victorian Family Home",
        "description": "Beautifully restored Victorian home with original architectural details. Wrap-around porch, updated kitchen with stainless steel appliances, and a spacious backyard perfect for entertaining.",
        "price": 675000,
        "property_type": PropertyType.HOUSE,
        "bedrooms": 4,
        "bathrooms": 3,
        "area_sqft": 2800,
        "address": "789 Oak Avenue",
        "city": "Austin",
        "state": "TX",
        "zip_code": "78704",
        "latitude": 30.2490,
        "longitude": -97.7656,
        "features": {"wrap_around_porch": True, "updated_kitchen": True, "backyard": True, "garage": True, "fireplace": True},
        "images": ["https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=800"],
        "year_built": 1920,
        "lot_size_sqft": 8500,
        "parking_spaces": 2,
    },
    {
        "title": "Luxury Waterfront Condo",
        "description": "Exclusive waterfront living with private balcony overlooking the lake. Resort-style amenities including infinity pool, spa, and private marina access. Smart home technology throughout.",
        "price": 1250000,
        "property_type": PropertyType.CONDO,
        "bedrooms": 3,
        "bathrooms": 3,
        "area_sqft": 2200,
        "address": "100 Lakefront Drive, PH-1",
        "city": "Miami",
        "state": "FL",
        "zip_code": "33101",
        "latitude": 25.7617,
        "longitude": -80.1918,
        "features": {"waterfront": True, "pool": True, "spa": True, "smart_home": True, "marina": True, "balcony": True},
        "images": ["https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800"],
        "year_built": 2022,
        "parking_spaces": 2,
        "hoa_monthly": 850,
    },
    {
        "title": "Cozy Starter Home in Great School District",
        "description": "Perfect starter home in a family-friendly neighborhood. Close to top-rated schools, parks, and shopping. Move-in ready with fresh paint and new carpeting.",
        "price": 295000,
        "property_type": PropertyType.HOUSE,
        "bedrooms": 3,
        "bathrooms": 2,
        "area_sqft": 1600,
        "address": "2345 Elm Street",
        "city": "Denver",
        "state": "CO",
        "zip_code": "80220",
        "latitude": 39.7392,
        "longitude": -104.9528,
        "features": {"near_schools": True, "fenced_yard": True, "new_paint": True, "garage": True},
        "images": ["https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800"],
        "year_built": 2005,
        "lot_size_sqft": 6000,
        "parking_spaces": 2,
    },
    {
        "title": "Sleek Urban Studio Apartment",
        "description": "Efficient and stylish studio in a trendy neighborhood. Exposed brick walls, modern kitchen, and in-unit washer/dryer. Walking distance to restaurants, bars, and public transit.",
        "price": 225000,
        "property_type": PropertyType.APARTMENT,
        "bedrooms": 0,
        "bathrooms": 1,
        "area_sqft": 550,
        "address": "567 Broadway, Unit 4C",
        "city": "New York",
        "state": "NY",
        "zip_code": "10012",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "features": {"exposed_brick": True, "in_unit_laundry": True, "near_transit": True, "rooftop_access": True},
        "images": ["https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800"],
        "year_built": 2015,
        "hoa_monthly": 550,
    },
    {
        "title": "Spacious Ranch with Pool",
        "description": "Single-story ranch home with open floor plan. Large backyard with heated pool and outdoor kitchen. Three-car garage with workshop space. Energy-efficient solar panels installed.",
        "price": 520000,
        "property_type": PropertyType.HOUSE,
        "bedrooms": 4,
        "bathrooms": 3,
        "area_sqft": 3200,
        "address": "8901 Desert Rose Lane",
        "city": "Phoenix",
        "state": "AZ",
        "zip_code": "85001",
        "latitude": 33.4484,
        "longitude": -112.0740,
        "features": {"pool": True, "outdoor_kitchen": True, "solar_panels": True, "workshop": True, "rv_parking": True},
        "images": ["https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=800"],
        "year_built": 2018,
        "lot_size_sqft": 15000,
        "parking_spaces": 3,
    },
    {
        "title": "Townhouse Near Tech Hub",
        "description": "Modern townhouse minutes from major tech campuses. Open living area, rooftop deck, and attached two-car garage. Community features include trails and a dog park.",
        "price": 780000,
        "property_type": PropertyType.TOWNHOUSE,
        "bedrooms": 3,
        "bathrooms": 2,
        "area_sqft": 1900,
        "address": "1234 Innovation Way",
        "city": "San Jose",
        "state": "CA",
        "zip_code": "95110",
        "latitude": 37.3382,
        "longitude": -121.8863,
        "features": {"rooftop_deck": True, "smart_home": True, "dog_park": True, "trails": True, "ev_charging": True},
        "images": ["https://images.unsplash.com/photo-1580587771525-78b9dba3b914?w=800"],
        "year_built": 2021,
        "parking_spaces": 2,
        "hoa_monthly": 400,
    },
    {
        "title": "Historic Brownstone in Back Bay",
        "description": "Elegant brownstone in Boston's prestigious Back Bay neighborhood. Period details include crown molding, built-in bookshelves, and marble fireplaces. Private garden patio.",
        "price": 1850000,
        "property_type": PropertyType.HOUSE,
        "bedrooms": 5,
        "bathrooms": 4,
        "area_sqft": 4500,
        "address": "234 Commonwealth Ave",
        "city": "Boston",
        "state": "MA",
        "zip_code": "02116",
        "latitude": 42.3601,
        "longitude": -71.0589,
        "features": {"crown_molding": True, "fireplace": True, "garden_patio": True, "wine_cellar": True, "library": True},
        "images": ["https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800"],
        "year_built": 1890,
        "lot_size_sqft": 3200,
        "parking_spaces": 1,
    },
    {
        "title": "Mountain View Cabin Retreat",
        "description": "Secluded cabin with stunning mountain views. A-frame design with vaulted ceilings, stone fireplace, and wraparound deck. Perfect for a weekend getaway or full-time mountain living.",
        "price": 425000,
        "property_type": PropertyType.HOUSE,
        "bedrooms": 2,
        "bathrooms": 2,
        "area_sqft": 1400,
        "address": "5678 Pine Ridge Road",
        "city": "Asheville",
        "state": "NC",
        "zip_code": "28801",
        "latitude": 35.5951,
        "longitude": -82.5515,
        "features": {"mountain_views": True, "fireplace": True, "deck": True, "hot_tub": True, "hiking_trails": True},
        "images": ["https://images.unsplash.com/photo-1518780664697-55e3ad937233?w=800"],
        "year_built": 2010,
        "lot_size_sqft": 43560,
        "parking_spaces": 2,
    },
    {
        "title": "Beachfront Investment Property",
        "description": "Prime beachfront property ideal for vacation rentals. Fully furnished with tropical decor. Strong rental history with average $3,500/month income. Walking distance to shops and restaurants.",
        "price": 595000,
        "property_type": PropertyType.CONDO,
        "bedrooms": 2,
        "bathrooms": 2,
        "area_sqft": 1100,
        "address": "321 Oceanfront Blvd, Unit 7B",
        "city": "San Diego",
        "state": "CA",
        "zip_code": "92101",
        "latitude": 32.7157,
        "longitude": -117.1611,
        "features": {"beachfront": True, "furnished": True, "ocean_view": True, "balcony": True, "pool": True},
        "images": ["https://images.unsplash.com/photo-1499793983690-e29da59ef1c2?w=800"],
        "year_built": 2016,
        "parking_spaces": 1,
        "hoa_monthly": 600,
    },
    {
        "title": "Contemporary Smart Home in Suburbs",
        "description": "Ultra-modern smart home with integrated automation system. Chef's kitchen with waterfall island, home theater, and heated floors. Energy-efficient design with geothermal heating.",
        "price": 890000,
        "property_type": PropertyType.HOUSE,
        "bedrooms": 5,
        "bathrooms": 4,
        "area_sqft": 4200,
        "address": "456 Technology Terrace",
        "city": "Seattle",
        "state": "WA",
        "zip_code": "98101",
        "latitude": 47.6062,
        "longitude": -122.3321,
        "features": {"smart_home": True, "home_theater": True, "heated_floors": True, "geothermal": True, "chef_kitchen": True, "ev_charging": True},
        "images": ["https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800"],
        "year_built": 2023,
        "lot_size_sqft": 12000,
        "parking_spaces": 3,
    },
    {
        "title": "Affordable Condo Near University",
        "description": "Well-maintained condo near the university campus. Great for students or rental investment. Community pool and fitness center. Low HOA fees. Recently updated bathroom and kitchen.",
        "price": 185000,
        "property_type": PropertyType.CONDO,
        "bedrooms": 1,
        "bathrooms": 1,
        "area_sqft": 750,
        "address": "890 College Avenue, Unit 2A",
        "city": "Austin",
        "state": "TX",
        "zip_code": "78705",
        "latitude": 30.2849,
        "longitude": -97.7341,
        "features": {"pool": True, "fitness_center": True, "near_university": True, "updated_kitchen": True},
        "images": ["https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=800"],
        "year_built": 2008,
        "parking_spaces": 1,
        "hoa_monthly": 200,
    },
]

# Real estate knowledge base entries
KNOWLEDGE_BASE = [
    {
        "id": "kb_hoa",
        "content": "HOA (Homeowners Association) is an organization in a subdivision, planned community, or condominium that makes and enforces rules for the properties and residents. HOA fees typically cover common area maintenance, amenities, exterior maintenance, and insurance. Monthly HOA fees can range from $100 to over $1,000 depending on the amenities and location.",
        "metadata": {"topic": "terminology", "keyword": "HOA"},
    },
    {
        "id": "kb_closing_costs",
        "content": "Closing costs are fees and expenses paid at the closing of a real estate transaction. They typically range from 2-5% of the purchase price. Common closing costs include: loan origination fees, appraisal fees, title insurance, attorney fees, home inspection, recording fees, and prepaid items like property taxes and homeowners insurance.",
        "metadata": {"topic": "buying", "keyword": "closing costs"},
    },
    {
        "id": "kb_cap_rate",
        "content": "Cap Rate (Capitalization Rate) is a key metric for evaluating rental property investments. It's calculated as Net Operating Income (NOI) divided by the property's current market value. A higher cap rate indicates a potentially higher return but also higher risk. Generally, cap rates of 4-6% are considered moderate, while 8-12% are considered high-yield but may indicate higher risk areas.",
        "metadata": {"topic": "investing", "keyword": "cap rate"},
    },
    {
        "id": "kb_mortgage_types",
        "content": "Common mortgage types include: 1) Fixed-Rate Mortgage: Interest rate stays the same for the entire loan term (15 or 30 years). 2) Adjustable-Rate Mortgage (ARM): Rate adjusts periodically based on market conditions. 3) FHA Loan: Government-backed, requires lower down payment (3.5%). 4) VA Loan: For veterans, often zero down payment. 5) Jumbo Loan: For amounts exceeding conforming loan limits.",
        "metadata": {"topic": "financing", "keyword": "mortgage types"},
    },
    {
        "id": "kb_inspection",
        "content": "A home inspection is a visual examination of a property's physical structure and systems. It typically covers: foundation, roof, plumbing, electrical, HVAC, insulation, windows, and appliances. A standard inspection costs $300-$500 and takes 2-4 hours. Always get an inspection before buying — it can reveal costly issues like foundation problems, roof damage, or mold.",
        "metadata": {"topic": "buying", "keyword": "home inspection"},
    },
    {
        "id": "kb_preapproval",
        "content": "Mortgage pre-approval is a lender's conditional commitment to lend you a specific amount. It requires a credit check, income verification, and financial documentation. Benefits include: knowing your budget, showing sellers you're serious, faster closing process. Pre-approval letters are typically valid for 60-90 days.",
        "metadata": {"topic": "financing", "keyword": "pre-approval"},
    },
    {
        "id": "kb_1031_exchange",
        "content": "A 1031 Exchange (like-kind exchange) allows real estate investors to defer capital gains taxes by reinvesting proceeds from a property sale into a similar property. Key rules: must identify replacement property within 45 days, close within 180 days, must be of equal or greater value, and must use a qualified intermediary. This is one of the most powerful tax strategies for real estate investors.",
        "metadata": {"topic": "investing", "keyword": "1031 exchange"},
    },
    {
        "id": "kb_credit_score",
        "content": "Credit score requirements for mortgages: Conventional loans typically require 620+, FHA loans require 580+ (3.5% down) or 500+ (10% down), VA loans have no minimum but most lenders prefer 620+, Jumbo loans typically require 700+. Higher credit scores qualify for better interest rates. For the best rates, aim for 760+. Improve your score by paying bills on time, keeping credit utilization below 30%, and avoiding new credit inquiries before applying.",
        "metadata": {"topic": "financing", "keyword": "credit score"},
    },
]


async def seed_database():
    """Seed the database with sample properties and knowledge base."""
    print("🌱 Seeding database...")

    # Initialize DB
    await init_db()

    async with async_session_factory() as db:
        # Check if already seeded
        from sqlalchemy import select, func
        count = await db.execute(select(func.count(Property.id)))
        existing = count.scalar()
        if existing and existing > 0:
            print(f"  Database already has {existing} properties. Skipping seed.")
            return

        # Insert properties
        for prop_data in SAMPLE_PROPERTIES:
            prop = Property(**prop_data)
            db.add(prop)

        await db.commit()
        print(f"  ✅ Inserted {len(SAMPLE_PROPERTIES)} properties")

    # Seed vector store
    print("  Indexing properties in ChromaDB...")
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
    print("🎉 Seeding complete!")


if __name__ == "__main__":
    asyncio.run(seed_database())
