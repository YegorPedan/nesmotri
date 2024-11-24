package models

import "time"

type AddPhone struct {
	StudentName    string    `json:"studentName"`
	PhoneModel     string    `json:"phoneModel"`
	PhoneCharge    int       `json:"charge"`
	ConnectionTime time.Time `json:"connectionTime"`
}
