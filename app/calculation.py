from datetime import datetime
import math
from . import constants

class FeeCalculator:
    @staticmethod
    def calculate_total_fee(cart_items) -> int:
        """
        Calculates the total fee for the given cart items.

        Args:
            cart_items (CartItems): The cart items object containing cart value, delivery distance, number of items and time.

        Returns:
            int: The total fee for the cart items.
        """
        if cart_items.cart_value >= constants.NO_FEE_THRESHOLD:
            return 0
        fee = 0
        fee += FeeCalculator.calculate_cart_value_fee(cart_items.cart_value)
        fee += FeeCalculator.calculate_distance_fee(cart_items.delivery_distance)
        fee += FeeCalculator.calculate_item_fee(cart_items.number_of_items)
        fee = FeeCalculator.apply_rush_hour_multiplier(cart_items.time, fee)
        return min(fee, constants.MAX_DELIVERY_FEE)

    @staticmethod
    def calculate_cart_value_fee(cart_value) -> int:
        """
        Calculate the fee for the cart value.

        If the cart value is less than 10 euros, the difference between the minimum purchase
        and the cart value is added to the result.

        Args:
            cart_value (int): The value of the cart.

        Returns:
            int: The fee for the cart value.
        """
        if cart_value < constants.MINIMUM_PURCHASE:
            return constants.MINIMUM_PURCHASE - cart_value
        return 0

    @staticmethod
    def calculate_distance_fee(delivery_distance) -> int:
        """
        Calculate the delivery fee based on the delivery distance.

        Args:
            delivery_distance (int): The distance of the delivery in meters.

        Returns:
            int: The calculated delivery fee in euros.

        Notes:
            - If the delivery distance is below 1000 meters, the fee is 2 euros.
            - For every 500 meters or less above 1000 meters, an additional 1 euro is added to the fee.
            - The base fee for delivery is 2 euros.

        """
        if delivery_distance <= constants.DISTANCE_THRESHOLD:
            return constants.BASE_FEE
        extra_distance = delivery_distance - constants.DISTANCE_THRESHOLD
        return constants.BASE_FEE + (math.ceil(extra_distance / 500) * 100)

    @staticmethod
    def calculate_item_fee(number_of_items) -> int:
        """
        Calculate the fee for a given number of items.

        Args:
            number_of_items (int): The number of items.

        Returns:
            int: The fee for the items.
        """
        if number_of_items <= constants.MINIMUM_ITEMS:
            return 0
        extra_items_fee = (number_of_items - constants.MINIMUM_ITEMS) * 50
        if number_of_items > constants.BULK_PACKAGE:
            extra_items_fee += constants.BULK_PACKAGE_FEE
        return extra_items_fee

    @staticmethod
    def is_rush_hour(datetime_object) -> bool:
        """
        Check if the given datetime object falls within the rush hour period on Fridays.

        Args:
            datetime_object (datetime): The datetime object to check.

        Returns:
            bool: True if the datetime falls within the rush hour period on Fridays, False otherwise.
        """
        start_rushhour = datetime.strptime("15:00:00", "%H:%M:%S").time()
        end_rushhour = datetime.strptime("19:00:00", "%H:%M:%S").time()
        return datetime_object.strftime("%A") == "Friday" and start_rushhour <= datetime_object.time() <= end_rushhour

    @staticmethod
    def apply_rush_hour_multiplier(datetime_object, delivery_fee) -> int:
        """
        Multiplies the delivery fee by 1.2x if the delivery time is during the rush hour period on Fridays.

        During the Friday rush, from 3 PM to 7 PM,
        the delivery fee (the total fee including possible surcharges)
        will be multiplied by 1.2x.

        Args:
            datetime_object (datetime): The datetime object representing the delivery time.
            delivery_fee (int): The original delivery fee.

        Returns:
            int: The updated delivery fee after applying the rush hour multiplier.
        """
        if FeeCalculator.is_rush_hour(datetime_object):
            return int(delivery_fee * constants.RUSH_HOURE_PERCENTAGE)
        return delivery_fee
