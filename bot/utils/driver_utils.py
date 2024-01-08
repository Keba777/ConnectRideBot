def format_ride_info(ride_request):
    passenger_info = ride_request.get('user', {})
    current_location = ride_request.get('currentLocation', '')
    destination = ride_request.get('destination', '')

    ride_info = (
        "👤 <b>Passenger Details</b>\n"
        f"<b>Name: </b> {passenger_info.get('fullName', '')}\n"
        f"<b>Phone: </b> {passenger_info.get('phone', '')}\n"
        f"<b>Departure: </b> {current_location}\n"
        f"<b>Destination: </b> {destination}\n"
    )
    return ride_info


def filter_rides_by_status(rides, status):
    filtered_rides = [ride for ride in rides if ride.get('status') == status]
    return filtered_rides
