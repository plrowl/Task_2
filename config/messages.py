class Messages:
    #Auth
    USER_ALREADY_EXISTS = "User already exists"
    MISSING_FIELD = "Email, password and name are required fields"
    INVALID_CREDENTIALS = "email or password are incorrect"
    UNAUTHORIZED = "You should be authorised"

    #User Update
    SUCCESS = "User data successfully updated"
    NOT_AUTHORIZED = "You should be authorised"

    #Orders
    EMPTY_INGREDIENTS = "Ingredient ids must be provided"
    INVALID_HASH = "One or more ids provided are incorrect" 
    SERVER_ERROR = "Internal Server Error"