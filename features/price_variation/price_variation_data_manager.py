def calculate_price_variation_costs(original_quantity, new_quantity, unit_rate):
    cost_at_same_rate = 0
    cost_at_98_percent = 0
    cost_at_96_percent = 0

    # Calculate thresholds
    qty_125_percent = original_quantity * 1.25
    qty_140_percent = original_quantity * 1.40
    qty_150_percent = original_quantity * 1.50

    # Quantities for new columns
    quantity_upto_125 = 0
    quantity_upto_140 = 0
    quantity_upto_150 = 0

    if new_quantity <= qty_125_percent:
        cost_at_same_rate = new_quantity * unit_rate
        quantity_upto_125 = new_quantity
    else:
        cost_at_same_rate = qty_125_percent * unit_rate
        quantity_upto_125 = qty_125_percent
        remaining_qty = new_quantity - qty_125_percent

        if new_quantity <= qty_140_percent:
            cost_at_98_percent = remaining_qty * unit_rate * 0.98
            quantity_upto_140 = remaining_qty
        else:
            cost_at_98_percent = (qty_140_percent - qty_125_percent) * unit_rate * 0.98
            quantity_upto_140 = (qty_140_percent - qty_125_percent)
            remaining_qty -= (qty_140_percent - qty_125_percent)

            if new_quantity <= qty_150_percent:
                cost_at_96_percent = remaining_qty * unit_rate * 0.96
                quantity_upto_150 = remaining_qty
            else:
                cost_at_96_percent = (qty_150_percent - qty_140_percent) * unit_rate * 0.96
                quantity_upto_150 = (qty_150_percent - qty_140_percent)
                # If new_quantity exceeds 150%, the cost for the quantity above 150% is not specified.
                # For now, we'll assume it's also at 96% or handle as an error/warning.
                # Based on the prompt, it only goes up to 150%.
                # If it goes beyond 150%, the prompt doesn't specify the rate.
                # For now, I'll cap the calculation at 150% as per the prompt.
                # Any quantity beyond 150% will not be factored into the reduced cost.
                # If the user wants to handle quantities beyond 150%, they need to specify the rate.

    total_cost_after = cost_at_same_rate + cost_at_98_percent + cost_at_96_percent

    return {
        "total_cost_after": total_cost_after,
        "quantity_upto_125": quantity_upto_125,
        "quantity_upto_140": quantity_upto_140,
        "quantity_upto_150": quantity_upto_150
    }
