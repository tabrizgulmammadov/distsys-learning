package main

import (
	"fmt"
	"log"
	"sync/atomic"

	maelstrom "github.com/jepsen-io/maelstrom/demo/go"
)

type generateOK struct {
	Type string `json:"type"`
	ID   string `json:"id"`
}

func main() {
	node := maelstrom.NewNode()
	var counter atomic.Int64

	node.Handle("generate", func(msg maelstrom.Message) error {
		return node.Reply(msg, generateOK{
			Type: "generate_ok",
			ID:   fmt.Sprintf("%s-%d", node.ID(), counter.Add(1)),
		})
	})

	if err := node.Run(); err != nil {
		log.Fatal(err)
	}
}
