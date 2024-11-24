package server

import (
	"github.com/labstack/echo/v4"
	"github.com/labstack/gommon/log"
	"mospolytech_app/config"
	"mospolytech_app/database"
)

func NewEchoServer(conf *config.Config, db database.Database) Server {
	echoApp := echo.New()
	echoApp.Logger.SetLevel(log.DEBUG)

	return &echoServer{
		app:  echoApp,
		db:   db,
		conf: conf,
	}
}
