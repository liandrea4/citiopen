import React from "react";
import { Link, Grid, Typography } from "@mui/material";

export default function ForgotPasswordComplete(props) {
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
            <Typography variant="h4">Password reset complete!</Typography>
          </Grid>
          <Grid item xs={12}>
            <Typography variant="body1">
              Your password has been reset. You can log in now with your new
              password.
            </Typography>
          </Grid>

          <Grid item xs={12}>
            <Link variant="body1" href="/login">
              Log in
            </Link>
          </Grid>
        </Grid>
      </div>
    </div>
  );
}
