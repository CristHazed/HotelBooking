class HotelBookingError(Exception):
    # Parent of all our custom errors
    pass

# ---------------- GUEST ---------------- 
class InvalidGuestNameError(HotelBookingError):
    pass

class InvalidContactError(HotelBookingError):
    pass

# ---------------- PACKS / ADD-ONS ---------------- 
class InvalidPackError(HotelBookingError):
    pass

class InvalidPackQuantityError(HotelBookingError):
    pass

class InvalidParticipantsCount(HotelBookingError):
    pass

# ---------------- ROOMS / STAY ---------------- 
class InvalidRoomSelectionError(HotelBookingError):
    pass

class InvalidStayDurationError(HotelBookingError):
    pass

class OccupiedRoomBookingError(HotelBookingError):
    pass