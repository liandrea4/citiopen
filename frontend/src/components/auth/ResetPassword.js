import React, { useState } from "react";
import { Grid, Typography, TextField, Button } from "@mui/material";

export default function ResetPassword(props) {
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

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
            <Typography component="h4" variant="h4">
              Reset Password
            </Typography>
          </Grid>
          <Grid item xs={12}>
            <TextField
              label="New Password"
              name="newPassword"
              variant="standard"
              required={true}
              onChange={(e) => setPassword(e.target.value)}
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              label="Confirm New Password"
              name="confirmPassword"
              variant="standard"
              required={true}
              onChange={(e) => setConfirmPassword(e.target.value)}
            />
          </Grid>

          <Grid item xs={12}>
            <Button
              color="primary"
              variant="contained"
              onClick={(e) =>
                fetch("/accounts/get-token", {
                  method: "POST",
                  headers: { "Content-Type": "application/json" },
                  body: JSON.stringify({
                    password: password,
                    confirmPassword: confirmPassword,
                  }),
                })
                  .then((response) => response.json())
                  .then((data) => console.log(data))
                  .catch((error) => {})
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
