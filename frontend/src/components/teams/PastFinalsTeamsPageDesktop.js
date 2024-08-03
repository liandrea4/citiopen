import React, { useState, useEffect } from "react";

import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import TextField from "@mui/material/TextField";

import { Banners, getAuthHeader, getCurrentYear } from "../Utils";
import { MATCH_TYPES } from "../Consts";
import { Header, renderTeams } from "./FinalsTeamsPageChairpersonUtils";

export default function PastFinalsTeamsPageDesktop() {
  const [year, setYear] = useState(getCurrentYear() - 1);
  const [ballkids, setBallkids] = useState([]);

  const [updated, setUpdated] = useState(false);

  const [showHovercard, setShowHovercard] = useState(false);

  const teams = Object.keys(MATCH_TYPES).map((key) => MATCH_TYPES[key]);

  useEffect(() => {
    fetch(`/api/get-past-finals/${year}`, { headers: getAuthHeader() })
      .then((response) => response.json())
      .then((data) =>
        setBallkids(data.filter((history) => history.year === year))
      );
  }, [year]);

  return (
    <div className="page">
      <Banners />

      <Grid container className="justify-top">
        <Grid
          item
          sm={6}
          md={7}
          lg={8}
          xl={9}
          style={{ maxHeight: "85vh", overflow: "auto" }}
        >
          <Box className="sxs">
            <Typography variant="h4">Past Finals Teams</Typography>
            &thinsp;
          </Box>

          <Box className="sxs">
            <Typography variant="body1">
              Showing finals for: &thinsp;
            </Typography>
            <TextField
              variant="standard"
              value={year}
              type="number"
              sx={{ mx: 2, maxWidth: "100px" }}
              onChange={(e) => setYear(e.target.value)}
            />
          </Box>
          {renderTeams(ballkids, teams, showHovercard, setUpdated)}
        </Grid>
      </Grid>
    </div>
  );
}
