def format_ride_info(ride_request):
    status = ride_request.get('status', '')
    current_location = ride_request.get('currentLocation', '')
    destination = ride_request.get('destination', '')

    if status == 'requested':
        ride_info = (
            "🚗  <b>Ride Details</b>\n"
            f"<b>Departure: </b> {current_location}\n"
            f"<b>Destination: </b> {destination}\n"
            f"<b>Status: </b> {status}\n"
        )
    elif status == 'accepted':
        driver_info = ride_request.get('driver', {})
        ride_info = (
            "🚗  <b>Ride Details</b>\n"
            f"<b>Driver: </b> {driver_info.get('fullName', '')}\n"
            f"<b>Phone: </b> {driver_info.get('phone', '')}\n"
            f"<b>Departure: </b> {current_location}\n"
            f"<b>Destination: </b> {destination}\n"
            f"<b>Status: </b> {status}\n"
        )
    else:
        driver_info = ride_request.get('driver', {})
        ride_info = (
            "🚗  <b>Ride Details</b>\n"
            f"<b>Driver: </b> {driver_info.get('fullName', '')}\n"
            f"<b>Phone: </b> {driver_info.get('phone', '')}\n"
            f"<b>Departure: </b> {current_location}\n"
            f"<b>Destination: </b> {destination}\n"
        )

    return ride_info
