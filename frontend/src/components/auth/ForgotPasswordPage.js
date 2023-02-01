import React, { useState } from "react";
import { Button, Grid, Typography, TextField } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { Alerts, handleChange, setSessionStorage } from "../Utils";

function submitPassword(state, setSuccessMsg, setErrorMsg, setToken, navigate) {
  fetch("/accounts/get-token", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      username: state.username,
      password: state.password,
    }),
  })
    .then((response) => {
      if (response.ok) {
        setSuccessMsg("Logged in");
        navigate("/");
      } else {
        setErrorMsg("Incorrect password.");
        throw new Error("Incorrect password");
      }
      return response.json();
    })
    .then((data) => {
      setToken(data?.token ?? "");
      setSessionStorage("group", data?.group ?? "");
      console.log(data);
      setSessionStorage("username", state?.username ?? "");
      setSessionStorage("ballkid_id", data?.ballkid_id ?? "");
    })
    .catch((error) => {});
}

export default function ForgotPasswordPage(props) {
  const [state, setState] = useState({
    username: "",
    password: "",
  });

  const [successMsg, setSuccessMsg] = useState("");
  const [errorMsg, setErrorMsg] = useState("");

  const setToken = props.setToken;
  const navigate = useNavigate();

  return (
    <div className="page">
      <div className="center">
        <Grid
          container
          spacing={2}
          alignItems="center"
          direction="column"
          justifyContent="center"
        >
          <Grid item xs={12}>
            <Alerts
              successMsg={successMsg}
              errorMsg={errorMsg}
              setSuccessMsg={setSuccessMsg}
              setErrorMsg={setErrorMsg}
            />
          </Grid>
          <Grid item xs={12}>
            <Typography component="h4" variant="h4">
              Forgot Password
            </Typography>
          </Grid>

          <Grid item xs={12}>
            <TextField
              label="Email"
              name="email"
              variant="standard"
              required={true}
              onChange={(e) => handleChange(e, state, setState)}
            />
          </Grid>
          <Grid item xs={12}>
            <Button
              color="primary"
              variant="contained"
              onClick={(e) =>
                submitPassword(
                  state,
                  setSuccessMsg,
                  setErrorMsg,
                  setToken,
                  navigate
                )
              }
            >
              Submit
            </Button>
          </Grid>
        </Grid>
      </div>
    </div>
  );
}
