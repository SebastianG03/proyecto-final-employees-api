from fastapi.responses import JSONResponse
from fastapi import status


unauthorized_access_response: JSONResponse = JSONResponse(
    status_code=status.HTTP_401_UNAUTHORIZED, 
    content={"message": "Unauthorized Access"})

internal_server_error_response: JSONResponse = lambda message: JSONResponse(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
    content={"message": message}
)

invalid_format_error_response: JSONResponse = lambda message: JSONResponse(
    status_code=status.HTTP_502_BAD_GATEWAY, 
    content={"message": message}
)

object_not_found_error: JSONResponse = lambda message: JSONResponse(
    status_code=status.HTTP_404_NOT_FOUND, 
    content={"message": message}
)


## General responses
created_response: JSONResponse = lambda message: JSONResponse(
    status_code=status.HTTP_201_CREATED, 
    content={"message": message}
)

successful_fetch_response: JSONResponse = lambda message: JSONResponse(
    status_code=status.HTTP_200_OK,
    content={"message": message}
)


#Auth responses
invalid_tokens_response: JSONResponse = JSONResponse(
    status_code=status.HTTP_400_BAD_REQUEST, 
    content={"message": "Invalid email or password"}
)
login_successful_response: JSONResponse = lambda user_data:JSONResponse(
    status_code=status.HTTP_200_OK, 
    content={"user": user_data}
)

user_exists_response: JSONResponse = JSONResponse(
    status_code=status.HTTP_400_BAD_REQUEST, 
    content={"message": "User already exists"}
)

not_logged_response: JSONResponse = JSONResponse(
    status_code=status.HTTP_401_UNAUTHORIZED, 
    content={"message": "Not Logged In"})

already_logged_response: JSONResponse = JSONResponse(
    status_code=status.HTTP_400_BAD_REQUEST, 
    content={"message": "You are already logged. Log out before create an account"})

### Toma un bool como argumento, si esta loggeado es True, caso contrario False. Devolvera un JSON con el mensaje
### correspondiente
logout_response: JSONResponse = lambda logged: JSONResponse(
            status_code=status.HTTP_200_OK, 
            content={"message": "Logout Successfully"}) if logged else JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                content={"message": "You are not logged. Try logging in first"})