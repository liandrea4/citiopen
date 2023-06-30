import React, { useState, useEffect } from "react";
import { useDrag, useDrop } from "react-dnd";
import { Link as RouterLink } from "react-router-dom";

import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import Divider from "@mui/material/Divider";
import IconButton from "@mui/material/IconButton";
import Button from "@mui/material/Button";
import Link from "@mui/material/Link";
import Paper from "@mui/material/Paper";

import Close from "@mui/icons-material/Close";
import SwapVert from "@mui/icons-material/SwapVert";

import {
  getAuthHeader,
  Icons,
  Alerts,
  SearchAndFilter,
  filterBallkids,
  HideShowToggle,
  isCurrentHour,
  CourtAssignment,
} from "../Utils";
import { MARGINS, ON_COURT_GREEN } from "../Consts";

function DraggableBallkidAndIcon(props) {
  const ballkid = props.ballkid;
  const [{ isDragging }, drag] = useDrag(() => ({
    type: "ballkid",
    item: { ...ballkid },
    collect: (monitor) => ({ isDragging: monitor.isDragging() }),
  }));

  return (
    <div
      ref={drag}
      style={{
        opacity: isDragging ? 0.5 : 1,
      }}
    >
      <div className="sxs">
        <Link
          variant="body2"
          component={RouterLink}
          to={`/ballkid/${ballkid.id}`}
        >
          {ballkid.first_name} {ballkid.last_name}
        </Link>
        &thinsp;
        <Icons ballkid={ballkid} margin={0} />
      </div>
    </div>
  );
}

function renderBallkidsOnTeam(assigned, teamNum, position, setUpdated) {
  return (
    <div>
      {assigned.map((ballkid) =>
        ballkid.current_team === teamNum && ballkid.position === position ? (
          <div key={`ballkid${ballkid.id}`} className="justify">
            {<DraggableBallkidAndIcon ballkid={ballkid} />}
            <div className="sxs">
              {!ballkid.preferred_position.includes("/") ? (
                ""
              ) : (
                <Button
                  variant="outlined"
                  size="small"
                  onClick={(e) => {
                    fetch("/api/update-ballkid", {
                      method: "PATCH",
                      headers: getAuthHeader(),
                      body: JSON.stringify({
                        first_name: ballkid.first_name,
                        last_name: ballkid.last_name,
                        position: ballkid.position === "Back" ? "Net" : "Back",
                      }),
                    })
                      .then((response) => response.json())
                      .then(() => setUpdated(true));
                  }}
                >
                  <SwapVert />
                </Button>
              )}
              <IconButton
                size="small"
                onClick={(e) => {
                  fetch("/api/update-ballkid", {
                    method: "PATCH",
                    headers: getAuthHeader(),
                    body: JSON.stringify({
                      first_name: ballkid.first_name,
                      last_name: ballkid.last_name,
                      current_team: 0,
                    }),
                  })
                    .then((response) => response.json())
                    .then(() => setUpdated(true));
                }}
              >
                <Close />
              </IconButton>
            </div>
          </div>
        ) : (
          ""
        )
      )}
    </div>
  );
}

export function Team({ team, assigned, nextShifts, setUpdated }) {
  const positions = ["Net", "Back"];
  const isCurrentlyOn =
    nextShifts.length > 0 && isCurrentHour(nextShifts[0]["start"]);

  const [{ isOver }, dropRef] = useDrop({
    accept: "ballkid",
    drop: (ballkid) =>
      fetch("/api/update-ballkid", {
        method: "PATCH",
        headers: getAuthHeader(),
        body: JSON.stringify({
          first_name: ballkid.first_name,
          last_name: ballkid.last_name,
          current_team: team,
        }),
      })
        .then((response) => response.json())
        .then(() => setUpdated(true)),
    collect: (monitor) => ({ isOver: monitor.isOver() }),
  });

  return (
    <Grid item xs={12} sm={6} md={6} lg={4} xl={3} ref={dropRef}>
      <Card
        sx={{ mb: 2, backgroundColor: isCurrentlyOn ? ON_COURT_GREEN : "" }}
        elevation={isOver ? 10 : 1}
      >
        <CardContent>
          <div className="justify">
            <div className="sxs">
              <Typography variant="h6">Team {team}</Typography>
              <Typography variant="subtitle1" sx={{ ml: 1 }}>
                ({assigned.length})
              </Typography>
            </div>

            <Button
              size="small"
              onClick={(e) => {
                fetch("/api/clear-team", {
                  method: "PATCH",
                  headers: getAuthHeader(),
                  body: JSON.stringify({
                    current_team: team,
                  }),
                })
                  .then((response) => response.json())
                  .then(() => setUpdated(true));
              }}
            >
              Clear
            </Button>
          </div>

          <CourtAssignment nextShifts={nextShifts} />

          {positions.map((position) => (
            <div key={position}>
              <Divider sx={{ my: 1 }} />
              <div className="sxs">
                <Typography variant="subtitle1">{position}s</Typography>
                <Typography variant="subtitle2" sx={{ ml: 1 }}>
                  (
                  {
                    assigned.filter((ballkid) => ballkid.position === position)
                      .length
                  }
                  )
                </Typography>
              </div>
              {renderBallkidsOnTeam(assigned, team, position, setUpdated)}
            </div>
          ))}
        </CardContent>
      </Card>
    </Grid>
  );
}

function renderTeams(assigned, teams, nextShifts, setUpdated) {
  return assigned.length > 0 ? (
    <Grid container spacing={2}>
      {teams.map((team) => (
        <Team
          key={team}
          team={team}
          assigned={assigned.filter((ballkid) => ballkid.current_team === team)}
          nextShifts={nextShifts.filter((shift) => shift.team === team)}
          setUpdated={setUpdated}
        />
      ))}
    </Grid>
  ) : (
    <Typography variant="body1">
      There are currently no teams assigned.
    </Typography>
  );
}

function Unassigned({ unassigned, setUpdated }) {
  const [searchKeyword, setSearchKeyword] = useState("");
  const [filterGroup, setFilterGroup] = useState();

  const positions = ["Net", "Back"];

  const [{ isOver }, dropRef] = useDrop({
    accept: "ballkid",
    drop: (ballkid) =>
      fetch("/api/update-ballkid", {
        method: "PATCH",
        headers: getAuthHeader(),
        body: JSON.stringify({
          first_name: ballkid.first_name,
          last_name: ballkid.last_name,
          current_team: 0,
        }),
      })
        .then((response) => response.json())
        .then(() => setUpdated(true)),
    collect: (monitor) => ({ isOver: monitor.isOver() }),
  });

  return (
    <Box
      component={Paper}
      ref={dropRef}
      elevation={isOver ? 10 : 1}
      sx={{ pl: { xs: 0, md: 3 }, ml: { xs: 0, md: 3 } }}
    >
      <div className="sxs">
        <Typography variant="h5" sx={MARGINS}>
          Unassigned
        </Typography>
        <Typography variant="h6" sx={MARGINS}>
          &ensp; (
          {filterBallkids(unassigned, searchKeyword, filterGroup).length})
        </Typography>
      </div>

      <div>
        <SearchAndFilter
          setSearchKeyword={setSearchKeyword}
          filterGroup={filterGroup}
          setFilterGroup={setFilterGroup}
          filters={["captain", "rookie", "chairperson"]}
        />
        {positions.map((position) => {
          const ballkids = filterBallkids(
            unassigned,
            searchKeyword,
            filterGroup
          ).filter((ballkid) => ballkid.preferred_position.includes(position));
          return (
            <div>
              <div className="sxs">
                <Typography variant="h6" sx={MARGINS}>
                  {position}s
                </Typography>
                <Typography variant="subtitle1" sx={{ ...MARGINS, ml: 1 }}>
                  ({ballkids.length})
                </Typography>
              </div>
              {ballkids.length === 0 ? (
                <Typography variant="body1" sx={{ pb: 1 }}>
                  There are currently no checked in {position.toLowerCase()}s
                  who are unassigned.
                </Typography>
              ) : (
                <Grid container>
                  {ballkids.map((ballkid) => (
                    <Grid item sm={3} md={6} sx={{ px: 1 }}>
                      {<DraggableBallkidAndIcon ballkid={ballkid} />}
                    </Grid>
                  ))}
                </Grid>
              )}
            </div>
          );
        })}
      </div>
    </Box>
  );
}

function Header() {
  const [successMsg, setSuccessMsg] = useState("");
  const [errorMsg, setErrorMsg] = useState("");

  return (
    <div>
      <Alerts
        successMsg={successMsg}
        errorMsg={errorMsg}
        setSuccessMsg={setSuccessMsg}
        setErrorMsg={setErrorMsg}
      />
      <div className="justify" style={{ marginBottom: 10 }}>
        <Typography variant="h4">Current Teams</Typography>
        <HideShowToggle
          teamType=""
          setSuccessMsg={setSuccessMsg}
          setErrorMsg={setErrorMsg}
        />
      </div>
    </div>
  );
}

export default function TeamsPageChairperson(props) {
  const [assigned, setAssigned] = useState([]);
  const [unassigned, setUnassigned] = useState([]);
  const [nextShifts, setNextShifts] = useState([]);
  const [teams, setTeams] = useState([]);
  const [updated, setUpdated] = useState(false);

  useEffect(() => {
    fetch("/api/sorted-list", { headers: getAuthHeader() })
      .then((response) => response.json())
      .then((data) => {
        setAssigned(
          data.filter(
            (ballkid) =>
              ballkid.is_checked_in === true && ballkid.current_team > 0
          )
        );
        setUnassigned(
          data.filter(
            (ballkid) =>
              ballkid.is_checked_in === true && ballkid.current_team === 0
          )
        );
      });

    fetch("/api/calc-num-teams", { headers: getAuthHeader() })
      .then((response) => response.json())
      .then((data) => setTeams(data["teams"]));

    fetch("/api/get-next-shifts", { headers: getAuthHeader() })
      .then((response) => response.json())
      .then((data) => setNextShifts(data))
      .then(() => setUpdated(false));
  }, [updated]);

  return (
    <div className="page">
      <Grid container className="justify-top">
        <Grid
          item
          sm={12}
          md={8}
          xl={9}
          style={{ maxHeight: "85vh", overflow: "auto" }}
        >
          <Header />
          {renderTeams(assigned, teams, nextShifts, setUpdated)}
        </Grid>
        {/* <Divider orientation="vertical" variant="middle" flexItem /> */}

        <Grid
          item
          sm={12}
          md={4}
          xl={3}
          style={{ maxHeight: "85vh", overflow: "auto" }}
        >
          <Unassigned unassigned={unassigned} setUpdated={setUpdated} />
        </Grid>
      </Grid>
    </div>
  );
}
