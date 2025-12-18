# utils/calculator.py
from .geoutils import haversine_distance

def calculate_delivery_cost(
    distance_km,
    base_fee=20,
    per_km_rate=10,
    surge_multiplier=1.0,
    discount_percent=0,
    min_total=30
):
    distance_cost = distance_km * per_km_rate
    subtotal = base_fee + distance_cost
    surcharged = subtotal * surge_multiplier
    discounted = surcharged * (1 - discount_percent / 100)
    total = max(discounted, min_total)
    
    return {
        "base_fee": base_fee,
        "distance_cost": round(distance_cost, 2),
        "subtotal": round(subtotal, 2),
        "surge_multiplier": surge_multiplier,
        "surge_amount": round(surcharged - subtotal, 2),
        "discount_percent": discount_percent,
        "discount_amount": round(surcharged - discounted, 2),
        "final_total": round(total, 2)
    }