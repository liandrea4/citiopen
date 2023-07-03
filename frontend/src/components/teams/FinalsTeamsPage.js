import React, { useState, useEffect } from "react";

import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Grid";
import Divider from "@mui/material/Divider";

import { getAuthHeader, BallkidAndIcon } from "../Utils";
import { MATCH_TYPES } from "../Consts";

function Team({ team, assigned }) {
  const positions = ["Net", "Back"];

  return (
    <Grid item xs={12} sm={6} md={4} lg={3} xl={2}>
      <Card sx={{ mb: 2 }}>
        <CardContent>
          <div className="justify">
            <div className="sxs">
              <Typography variant="h6">{team}</Typography>
              <Typography variant="subtitle1" sx={{ ml: 1 }}>
                (
                {
                  assigned.filter((ballkid) => ballkid.finals_team === team)
                    .length
                }
                )
              </Typography>
            </div>
          </div>

          {positions.map((position) => (
            <div key={position}>
              <Divider sx={{ mt: 1, mb: 1 }} />
              <div className="sxs">
                <Typography variant="subtitle1">{position}s</Typography>
                <Typography variant="subtitle2" sx={{ ml: 1 }}>
                  (
                  {
                    assigned.filter(
                      (ballkid) =>
                        ballkid.finals_team === team &&
                        ballkid.finals_position === position
                    ).length
                  }
                  )
                </Typography>
              </div>

              {assigned.map((ballkid) =>
                ballkid.finals_team === team &&
                ballkid.finals_position === position ? (
                  <BallkidAndIcon key={ballkid.id} ballkid={ballkid} />
                ) : (
                  ""
                )
              )}
            </div>
          ))}
        </CardContent>
      </Card>
    </Grid>
  );
}

export default function FinalsTeamsPage(props) {
  const [assigned, setAssigned] = useState([]);
  const [showFinalsTeams, setShowFinalsTeams] = useState(false);

  const teams = Object.keys(MATCH_TYPES).map((key) => MATCH_TYPES[key]);

  useEffect(() => {
    fetch("/api/sorted-list", { headers: getAuthHeader() })
      .then((response) => response.json())
      .then((data) =>
        setAssigned(data.filter((ballkid) => ballkid.finals_team))
      );

    fetch("/api/get-tournament", {
      method: "GET",
      headers: getAuthHeader(),
    })
      .then((response) => response.json())
      .then((data) => setShowFinalsTeams(data["show_finals_teams"]));
  }, []);

  return (
    <div className="page">
      <Typography variant="h4" sx={{ mb: 2 }}>
        Finals Teams
      </Typography>
      {assigned.length > 0 && showFinalsTeams ? (
        <Grid container spacing={2}>
          {teams.map((team) => (
            <Team key={team} team={team} assigned={assigned} />
          ))}
        </Grid>
      ) : (
        <Typography variant="body1">
          There are currently no finals teams assigned.
        </Typography>
      )}
    </div>
  );
}
