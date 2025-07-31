def calculate_price_variation_costs(original_quantity, new_quantity, unit_rate):
    cost_of_original_qty = original_quantity * unit_rate
    additional_cost = 0

    # Calculate thresholds for additional quantity
    threshold_125 = original_quantity * 0.25  # 25% of original
    threshold_140 = original_quantity * 0.40  # 40% of original
    threshold_150 = original_quantity * 0.50  # 50% of original

    # Quantities for new columns (these are the *incremental* quantities)
    quantity_upto_125 = 0
    quantity_upto_140 = 0
    quantity_upto_150 = 0

    qty_for_tier1 = 0
    qty_for_tier2 = 0
    qty_for_tier3 = 0
    remaining_increase = 0

    if new_quantity <= original_quantity:
        # No increase, so additional_cost is 0
        total_cost_after = new_quantity * unit_rate
        return {
            "total_cost_after": total_cost_after,
            "quantity_upto_125": 0,
            "quantity_upto_140": 0,
            "quantity_upto_150": 0,
            "cost_upto_125": 0,
            "cost_upto_140": 0,
            "cost_upto_150": 0
        }

    # Calculate the actual increase in quantity
    actual_increase = new_quantity - original_quantity

    # Tier 1: up to 25% of original quantity increase (i.e., total quantity up to 125% of original)
    qty_for_tier1 = min(actual_increase, threshold_125)
    additional_cost += qty_for_tier1 * unit_rate
    quantity_upto_125 = qty_for_tier1

    remaining_increase = actual_increase - qty_for_tier1

    if remaining_increase > 0:
        # Tier 2: from 25% to 40% of original quantity increase (i.e., total quantity from 125% to 140% of original)
        qty_for_tier2 = min(remaining_increase, (threshold_140 - threshold_125))
        additional_cost += qty_for_tier2 * unit_rate * 0.98
        quantity_upto_140 = qty_for_tier2

        remaining_increase -= qty_for_tier2

        if remaining_increase > 0:
            # Tier 3: from 40% to 50% of original quantity increase (i.e., total quantity from 140% to 150% of original)
            qty_for_tier3 = min(remaining_increase, (threshold_150 - threshold_140))
            additional_cost += qty_for_tier3 * unit_rate * 0.96
            quantity_upto_150 = qty_for_tier3

            remaining_increase -= qty_for_tier3

            if remaining_increase > 0:
                # If new_quantity exceeds 150% of original, the remaining quantity is also at 96% rate
                additional_cost += remaining_increase * unit_rate * 0.96
                quantity_upto_150 += remaining_increase


    total_cost_after = cost_of_original_qty + additional_cost

    return {
        "total_cost_after": total_cost_after,
        "quantity_upto_125": quantity_upto_125,
        "quantity_upto_140": quantity_upto_140,
        "quantity_upto_150": quantity_upto_150,
        "cost_upto_125": qty_for_tier1 * unit_rate,
        "cost_upto_140": qty_for_tier2 * unit_rate * 0.98,
        "cost_upto_150": (qty_for_tier3 + remaining_increase) * unit_rate * 0.96
    }
