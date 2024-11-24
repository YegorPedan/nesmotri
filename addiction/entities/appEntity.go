package entities

import "time"

type (
	Phone struct {
		Id                uint32    `gorm:"primaryKey;autoIncrement" json:"id"`
		StudentName       string    `json:"studentName"`
		PhoneModel        string    `json:"phoneModel"`
		PhoneCharge       int       `json:"charge"`
		ConnectionTime    time.Time `json:"connectionTime"`
		DisconnectionTime time.Time `json:"disconnectionTime"`
	}
)
