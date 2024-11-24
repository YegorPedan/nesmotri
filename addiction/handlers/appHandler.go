package handlers

import "github.com/labstack/echo/v4"

type AppHandler interface {
	InsertPhoneData(c echo.Context) error
	PickUpPhone(c echo.Context, id int) error
}
