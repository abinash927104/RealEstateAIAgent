"use client";

import { useState, useEffect } from "react";
import Navbar from "@/components/layout/Navbar";
import { propertiesApi, type PropertyData, type PropertySearchParams } from "@/lib/api";

const propertyTypes = [
  { value: "", label: "All Types" },
  { value: "house", label: "🏠 House" },
  { value: "apartment", label: "🏢 Apartment" },
  { value: "condo", label: "🏬 Condo" },
  { value: "townhouse", label: "🏘️ Townhouse" },
  { value: "land", label: "🌳 Land" },
];

export default function PropertiesPage() {
  const [properties, setProperties] = useState<PropertyData[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  // Filters
  const [city, setCity] = useState("");
  const [propertyType, setPropertyType] = useState("");
  const [minPrice, setMinPrice] = useState("");
  const [maxPrice, setMaxPrice] = useState("");
  const [minBedrooms, setMinBedrooms] = useState("");

  const fetchProperties = async (pageNum = 1) => {
    setLoading(true);
    try {
      const params: PropertySearchParams = {
        page: pageNum,
        page_size: 12,
        sort_by: "listed_at",
        sort_order: "desc",
      };
      if (city) params.city = city;
      if (propertyType) params.property_type = propertyType;
      if (minPrice) params.min_price = Number(minPrice);
      if (maxPrice) params.max_price = Number(maxPrice);
      if (minBedrooms) params.min_bedrooms = Number(minBedrooms);

      const data = await propertiesApi.list(params);
      setProperties(data.properties);
      setTotal(data.total);
      setTotalPages(data.total_pages);
      setPage(data.page);
    } catch {
      console.error("Failed to fetch properties");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProperties();
  }, []);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    fetchProperties(1);
  };

  const formatPrice = (price: number) => {
    if (price >= 1000000) return `$${(price / 1000000).toFixed(1)}M`;
    if (price >= 1000) return `$${(price / 1000).toFixed(0)}K`;
    return `$${price}`;
  };

  return (
    <>
      <Navbar />
      <div style={{ paddingTop: 64, minHeight: "100vh", background: "var(--color-surface)" }}>
        {/* Header */}
        <div
          style={{
            padding: "48px 24px 32px",
            textAlign: "center",
            background: "var(--color-surface-elevated)",
            borderBottom: "1px solid var(--color-border)",
          }}
        >
          <h1
            style={{
              fontSize: "clamp(1.8rem, 4vw, 2.5rem)",
              fontWeight: 800,
              marginBottom: 8,
              fontFamily: "var(--font-heading)",
            }}
          >
            Explore <span className="gradient-text">Properties</span>
          </h1>
          <p style={{ color: "var(--color-text-secondary)", fontSize: "1.05rem" }}>
            {total > 0 ? `${total} properties available` : "Search our listings"}
          </p>
        </div>

        {/* Filters */}
        <form
          onSubmit={handleSearch}
          style={{
            maxWidth: 1200,
            margin: "-20px auto 0",
            padding: "0 24px",
            position: "relative",
            zIndex: 10,
          }}
        >
          <div
            className="glass-card"
            style={{
              padding: 24,
              display: "flex",
              gap: 12,
              flexWrap: "wrap",
              alignItems: "flex-end",
            }}
          >
            <div style={{ flex: "1 1 180px" }}>
              <label style={{ fontSize: "0.8rem", color: "var(--color-text-muted)", marginBottom: 4, display: "block" }}>City</label>
              <input className="input" placeholder="e.g., Austin" value={city} onChange={(e) => setCity(e.target.value)} />
            </div>
            <div style={{ flex: "1 1 150px" }}>
              <label style={{ fontSize: "0.8rem", color: "var(--color-text-muted)", marginBottom: 4, display: "block" }}>Type</label>
              <select className="input" value={propertyType} onChange={(e) => setPropertyType(e.target.value)}>
                {propertyTypes.map((t) => (
                  <option key={t.value} value={t.value}>{t.label}</option>
                ))}
              </select>
            </div>
            <div style={{ flex: "1 1 130px" }}>
              <label style={{ fontSize: "0.8rem", color: "var(--color-text-muted)", marginBottom: 4, display: "block" }}>Min Price</label>
              <input className="input" type="number" placeholder="$0" value={minPrice} onChange={(e) => setMinPrice(e.target.value)} />
            </div>
            <div style={{ flex: "1 1 130px" }}>
              <label style={{ fontSize: "0.8rem", color: "var(--color-text-muted)", marginBottom: 4, display: "block" }}>Max Price</label>
              <input className="input" type="number" placeholder="$∞" value={maxPrice} onChange={(e) => setMaxPrice(e.target.value)} />
            </div>
            <div style={{ flex: "1 1 100px" }}>
              <label style={{ fontSize: "0.8rem", color: "var(--color-text-muted)", marginBottom: 4, display: "block" }}>Beds</label>
              <input className="input" type="number" placeholder="Any" min="0" value={minBedrooms} onChange={(e) => setMinBedrooms(e.target.value)} />
            </div>
            <button type="submit" className="btn-primary" style={{ padding: "12px 24px", height: 46 }}>
              🔍 Search
            </button>
          </div>
        </form>

        {/* Results */}
        <div style={{ maxWidth: 1200, margin: "32px auto", padding: "0 24px" }}>
          {loading ? (
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))",
                gap: 24,
              }}
            >
              {Array.from({ length: 6 }).map((_, i) => (
                <div key={i} className="skeleton" style={{ height: 360, borderRadius: 16 }} />
              ))}
            </div>
          ) : properties.length === 0 ? (
            <div
              style={{
                textAlign: "center",
                padding: "80px 24px",
                color: "var(--color-text-muted)",
              }}
            >
              <div style={{ fontSize: "3rem", marginBottom: 16 }}>🏠</div>
              <h3 style={{ fontSize: "1.3rem", marginBottom: 8, color: "var(--color-text-secondary)" }}>
                No properties found
              </h3>
              <p>Try adjusting your filters or search for a different location.</p>
            </div>
          ) : (
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))",
                gap: 24,
              }}
              className="stagger-children"
            >
              {properties.map((prop) => (
                <a
                  key={prop.id}
                  href={`/properties/${prop.id}`}
                  className="glass-card"
                  style={{
                    overflow: "hidden",
                    textDecoration: "none",
                    color: "inherit",
                    display: "flex",
                    flexDirection: "column",
                  }}
                >
                  {/* Image */}
                  <div
                    style={{
                      height: 200,
                      background: prop.images?.[0]
                        ? `url(${prop.images[0]}) center/cover`
                        : "linear-gradient(135deg, var(--color-primary-light), var(--color-primary-lighter))",
                      position: "relative",
                    }}
                  >
                    <div
                      style={{
                        position: "absolute",
                        top: 12,
                        right: 12,
                        padding: "4px 12px",
                        borderRadius: 9999,
                        background: "rgba(0,0,0,0.6)",
                        backdropFilter: "blur(8px)",
                        color: "white",
                        fontSize: "0.8rem",
                        fontWeight: 600,
                      }}
                    >
                      {prop.property_type}
                    </div>
                  </div>

                  {/* Details */}
                  <div style={{ padding: "16px 20px", flex: 1 }}>
                    <div
                      style={{
                        fontSize: "1.4rem",
                        fontWeight: 800,
                        fontFamily: "var(--font-heading)",
                        marginBottom: 6,
                      }}
                      className="gradient-text"
                    >
                      {formatPrice(prop.price)}
                    </div>
                    <h3 style={{ fontSize: "1rem", fontWeight: 600, marginBottom: 8, lineHeight: 1.3 }}>
                      {prop.title}
                    </h3>
                    <p style={{ color: "var(--color-text-muted)", fontSize: "0.85rem", marginBottom: 12 }}>
                      📍 {prop.address}, {prop.city}, {prop.state}
                    </p>
                    <div
                      style={{
                        display: "flex",
                        gap: 16,
                        color: "var(--color-text-secondary)",
                        fontSize: "0.85rem",
                      }}
                    >
                      {prop.bedrooms !== null && <span>🛏️ {prop.bedrooms} bd</span>}
                      {prop.bathrooms !== null && <span>🚿 {prop.bathrooms} ba</span>}
                      {prop.area_sqft && <span>📐 {prop.area_sqft.toLocaleString()} sqft</span>}
                    </div>
                  </div>
                </a>
              ))}
            </div>
          )}

          {/* Pagination */}
          {totalPages > 1 && (
            <div
              style={{
                display: "flex",
                justifyContent: "center",
                gap: 8,
                marginTop: 40,
                paddingBottom: 40,
              }}
            >
              {Array.from({ length: totalPages }, (_, i) => i + 1).map((p) => (
                <button
                  key={p}
                  onClick={() => fetchProperties(p)}
                  className={p === page ? "btn-primary" : "btn-secondary"}
                  style={{
                    padding: "8px 14px",
                    minWidth: 40,
                    fontSize: "0.85rem",
                  }}
                >
                  {p}
                </button>
              ))}
            </div>
          )}
        </div>
      </div>
    </>
  );
}
