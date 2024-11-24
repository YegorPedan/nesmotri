package main

import (
	"mospolytech_app/config"
	"mospolytech_app/database"
	"mospolytech_app/server"
)

func main() {
	conf := config.GetConfig()
	db := database.NewPostgresDatabase(conf)
	server.NewEchoServer(conf, db).Start()
}
