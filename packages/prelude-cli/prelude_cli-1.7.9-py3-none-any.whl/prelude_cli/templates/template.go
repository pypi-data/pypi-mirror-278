/*
ID: $ID
NAME: $NAME
UNIT: $UNIT
CREATED: $TIME
*/
package main

import (
	"github.com/preludeorg/libraries/go/tests/endpoint"
)

func test() {
	Endpoint.Stop(100)
}

func clean() {
	Endpoint.Say("Cleaning up")
}

func main() {
	Endpoint.Start(test, clean)
}
