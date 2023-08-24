package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"strconv"
)

func main() {
	build_url := os.Getenv("BUILD_URL")
	test_url := os.Getenv("TEST_URL")

	http.HandleFunc("/ping", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "pong")
	})

	http.HandleFunc("/run", func(w http.ResponseWriter, r *http.Request) {
		// Get the steps parameter from the query string.
		steps, err := strconv.Atoi(r.URL.Query().Get("steps"))
		if err != nil {
			fmt.Fprintf(w, "Invalid steps parameter: %v", err)
			return
		}

		// Make a request to the first API server.
		response, err := http.Get(build_url + "/build?steps=" + strconv.Itoa(steps))
		if err != nil {
			fmt.Fprintf(w, "Error making request to first API server: %v", err)
			return
		}

		defer response.Body.Close()
		body, err := ioutil.ReadAll(response.Body)
		if err != nil {
			fmt.Fprintf(w, "Error reading response from first API server: %v", err)
			return
		}

		// Make a request to the second API server.
		response, err = http.Get(test_url + "/test?steps=" + strconv.Itoa(steps))
		if err != nil {
			fmt.Fprintf(w, "Error making request to second API server: %v", err)
			return
		}

		defer response.Body.Close()
		body2, err := ioutil.ReadAll(response.Body)
		if err != nil {
			fmt.Fprintf(w, "Error reading response from second API server: %v", err)
			return
		}

		// Combine the responses from the two API servers.
		fmt.Fprintf(w, "build => %s\n test => %s", body, body2)
	})

	port := 8080
	fmt.Println("Serving on port", port)
	http.ListenAndServe(":"+strconv.Itoa(port), nil)
}
