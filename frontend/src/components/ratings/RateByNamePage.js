import React, { useState, useEffect } from "react";

import Typography from "@mui/material/Typography";
import Switch from "@mui/material/Switch";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";

import {
  LayoutButtons,
  getAuthHeader,
  RatingButton,
  getLocalStorage,
  useIsMobile,
  SearchAndFilter,
  filterBallkids,
  BallkidCard,
} from "../Utils";

function getBallkidsToRender(ballkids, showUnrated, showTeam, myTeam) {
  const pk = getLocalStorage("ballkid_id");

  var ballkidsToRender = ballkids;
  ballkidsToRender = !showUnrated
    ? ballkidsToRender
    : ballkidsToRender.filter(
        (ballkid) => !ballkid.have_rated && ballkid.id !== pk
      );
  ballkidsToRender = !showTeam
    ? ballkidsToRender
    : ballkidsToRender.filter((ballkid) => ballkid.current_team === myTeam);

  return ballkidsToRender;
}

function renderSwitch(param, setParam, offStr, onStr) {
  return (
    <Grid item className="sxs" xs={12} md={6} lg={5} xl={4}>
      <Typography variant="body1">{offStr}</Typography>
      <Switch checked={param} onClick={(e) => setParam(e.target.checked)} />
      <Typography variant="body1">{onStr}</Typography>
    </Grid>
  );
}

function BallkidsSection({ ballkids, gridLayout, setUpdated }) {
  const isMobile = useIsMobile();
  const isChairperson = getLocalStorage("group") === "chairperson";

  return ballkids.length === 0 ? (
    <Typography variant="body1">There are no ballkids to rate.</Typography>
  ) : (
    ballkids.map((ballkid) => (
      <Grid
        item
        key={ballkid.id}
        xs={gridLayout ? 6 : 12}
        sm={gridLayout ? 4 : 12}
        md={gridLayout ? 3 : 12}
        lg={gridLayout ? 2 : 12}
        xl={gridLayout ? 1 : 12}
      >
        <BallkidCard
          ballkid={ballkid}
          renderAdditional={
            <Box textAlign="center" sx={{ mt: gridLayout ? 1 : 0 }}>
              {ballkid.id === getLocalStorage("ballkid_id") ? (
                ""
              ) : (
                <RatingButton
                  ballkid={ballkid}
                  setUpdated={setUpdated}
                  isMobile={isMobile}
                />
              )}

              {!isChairperson ? (
                ""
              ) : (
                <Typography
                  variant="subtitle2"
                  sx={{ mt: gridLayout ? 0.5 : 0 }}
                >
                  Total ratings: {ballkid.num_ratings}
                </Typography>
              )}
            </Box>
          }
        />
      </Grid>
    ))
  );
}

export default function RateByNamePage(props) {
  const [ballkids, setBallkids] = useState([]);
  const [myTeam, setMyTeam] = useState();

  const [showUnrated, setShowUnrated] = useState(false);
  const [showTeam, setShowTeam] = useState(true);
  const [updated, setUpdated] = useState(false);

  const [searchKeyword, setSearchKeyword] = useState("");
  const [filterGroup, setFilterGroup] = useState();

  const [gridLayout, setGridLayout] = useState(
    getLocalStorage("gridLayout") ?? true
  );
  const pk = getLocalStorage("ballkid_id");

  useEffect(() => {
    fetch("/api/list/" + pk, {
      headers: getAuthHeader(),
    })
      .then((response) => response.json())
      .then((data) => {
        setBallkids(data);
        setMyTeam(data.filter((ballkid) => ballkid.id === pk)[0].current_team);
      })
      .then(() => setUpdated(false));
  }, [pk, updated]);

  return (
    <div className="page">
      <div className="justify">
        <div className="sxs">
          <Typography variant="h4" sx={{ mb: 1 }}>
            Rate by Name
          </Typography>

          <Typography variant="h6" sx={{ mb: 1 }}>
            &ensp; (
            {
              filterBallkids(
                getBallkidsToRender(ballkids, showUnrated, showTeam, myTeam),
                searchKeyword,
                filterGroup
              ).length
            }
            )
          </Typography>
        </div>
        <LayoutButtons gridLayout={gridLayout} setGridLayout={setGridLayout} />
      </div>

      <Grid container>
        {renderSwitch(
          showUnrated,
          setShowUnrated,
          "Show All Ballkids",
          "Show Ballkids to Rate"
        )}

        {renderSwitch(
          showTeam,
          setShowTeam,
          "Show All Teams",
          "Show My Team Only"
        )}
      </Grid>

      <Grid container spacing={gridLayout ? 2 : 1}>
        <SearchAndFilter
          setSearchKeyword={setSearchKeyword}
          filterGroup={filterGroup}
          setFilterGroup={setFilterGroup}
        />
        <BallkidsSection
          ballkids={filterBallkids(
            getBallkidsToRender(ballkids, showUnrated, showTeam, myTeam),
            searchKeyword,
            filterGroup
          )}
          gridLayout={gridLayout}
          setUpdated={setUpdated}
        />
      </Grid>
    </div>
  );
}
