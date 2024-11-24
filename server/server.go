package server

import (
	"fmt"
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
	"mospolytech_app/config"
	"mospolytech_app/database"
)

type Server interface {
	Start()
}

// echoServer
type echoServer struct {
	app  *echo.Echo
	db   database.Database
	conf *config.Config
}

func (s *echoServer) Start() {
	s.app.Use(middleware.Recover())
	s.app.Use(middleware.Logger())

	s.app.GET("v1/health", func(c echo.Context) error {
		return c.JSON(200, "OK")
	})

	serveUrl := fmt.Sprintf(":%d", s.conf.Server.Port)
	s.app.Logger.Fatal(s.app.Start(serveUrl))
}
