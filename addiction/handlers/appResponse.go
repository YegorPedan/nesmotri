package handlers

import (
	"github.com/labstack/echo/v4"
)

type baseResponse struct {
	Message string `json:"message"`
}

func response(c echo.Context, code int, message string) error {
	return c.JSON(code, &baseResponse{message})
}
