async function runtest() {
    let success = 0;
    let fail = 0;
    start = Date.now();
    for (let i = 0; i < 10000; i++) {
        await fetch("http://localhost:5001/notes", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization:
              "Bearer " +
              "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc3NjI0NDIyOSwianRpIjoiNjZiOTYzODQtNzBhYS00MDBhLTk3YmEtODhkMDVkZjQ3MGI4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IntcImlkXCI6IDE1LCBcInJvbGVcIjogXCJhZG1pblwifSIsIm5iZiI6MTc3NjI0NDIyOSwiY3NyZiI6ImQzNDM0YWFiLWUzZDUtNGZhZS04ZGZiLTYzYjE0OGYwNzQ1MyIsImV4cCI6MTc3NjI1MTQyOX0.JlbewYlOwltZJXpsWRiBQ1o9Br2kN7MmZdfl2c4e9mI",
          },
          body: JSON.stringify({
            title: "Speed Test Note",
            content: "This is a note created during the load test!",
          }),
        })
          .then((res) => res.json())
          .then((data) => {
            success++;
            console.log(data);
          })
          .catch((err) => {
            fail++;
            console.log(err);
          });
    }
    end = Date.now();
    console.log("Time: " + (end - start) / 1000 + "s");
    console.log("Success: " + success + " Fail: " + fail);
}
async function runtestgetall() {
    let success = 0;
    let fail = 0;
    start = Date.now();
    for (let i = 0; i < 3; i++) {
        await fetch("http://localhost:5001/allNotes", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                Authorization:
                    "Bearer " +
                    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc3NjE2ODg2OSwianRpIjoiYTkxMzJkNWItNmI2MC00MTk2LWFmN2UtZDA0MzNhZjkxMDRmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IntcImlkXCI6IDEsIFwicm9sZVwiOiBcImFkbWluXCJ9IiwibmJmIjoxNzc2MTY4ODY5LCJjc3JmIjoiMWZkMGE0NDEtODA5Ni00Njc4LWIzMWQtODQ0NzI3NGNhM2M3IiwiZXhwIjoxNzc2MTc2MDY5fQ.bd6jRyZHHNZq4nfLB0H9BUpAgeKPs5YRisdacsrmX_Q",
            },
        })
            .then((res) => res.json())
            .then((data) => {
                success++;
                console.log(data);
            })
            .catch((err) => {
                fail++;
                console.log(err);
            });
    }
    end = Date.now();
    console.log("Time: " + (end - start) / 1000 + "s");
    console.log("Success: " + success + " Fail: " + fail);
}

runtest();
// runtestgetall();
