import React, { useState } from "react";
import { Link } from "react-router-dom";
import {
  AppBar,
  Toolbar,
  Typography,
  Icon,
  Button,
  Menu,
  MenuItem,
} from "@mui/material";
import { SportsTennis } from "@mui/icons-material";
import { getSessionStorage, setSessionStorage } from "./Utils";

function NavbarItem({ tab }) {
  const [anchorEl, setAnchorEl] = useState(null);
  const [overButton, setOverButton] = useState(false);
  const [overMenu, setOverMenu] = useState(false);

  const handleClose = () => {
    setOverButton(false);
    setOverMenu(false);
  };

  const enterButton = (e) => {
    setOverButton(true);
    setAnchorEl(e.currentTarget);
  };

  const leaveButton = () => {
    // Set a timeout so that the menu doesn't close before the user has time to
    // move their mouse over it
    setTimeout(() => {
      setOverButton(false);
    }, 50);
  };

  const enterMenu = () => {
    setOverMenu(true);
  };

  const leaveMenu = () => {
    setOverMenu(false);
  };

  return (
    <div>
      <Button
        color="inherit"
        onMouseEnter={enterButton}
        onMouseLeave={leaveButton}
        component={Link}
        to={tab.url}
      >
        {tab.label}
      </Button>

      {/* {tab.subtabs ? <Dropdown subtabs={tab.subtabs} /> : ""} */}
      {!tab.subtabs ? (
        ""
      ) : (
        <Menu
          anchorEl={anchorEl}
          open={overButton || overMenu}
          sx={{
            pointerEvents: "none",
          }}
          disableRestoreFocus
          MenuListProps={{
            onMouseEnter: enterMenu,
            onMouseLeave: leaveMenu,
            style: { pointerEvents: "auto" },
          }}
        >
          {tab.subtabs.map((subtab) => (
            <MenuItem
              key={subtab.label}
              component={Link}
              to={subtab.url}
              onClick={handleClose}
            >
              {subtab.label}
            </MenuItem>
          ))}
        </Menu>
      )}
    </div>
  );
}

export default function Navbar(props) {
  const group = getSessionStorage("group");

  const ballkidTabs = [
    { label: "By Name", url: "/" },
    {
      label: "Teams",
      url: "/teams",
      subtabs: [
        { label: "Teams", url: "/teams" },
        { label: "Finals Teams", url: "/finals-teams" },
      ],
    },
    { label: "Schedule", url: "/schedule" },
  ];

  const captainTabs = [
    { label: "By Name", url: "/" },
    {
      label: "Teams",
      url: "/teams",
      subtabs: [
        { label: "Teams", url: "/teams" },
        { label: "Finals Teams", url: "/finals-teams" },
      ],
    },
    { label: "Schedule", url: "/schedule" },
    {
      label: "Ratings",
      url: "/rate",
      subtabs: [
        { label: "Rate By Name", url: "/rate" },
        { label: "Rate By Past Teams", url: "/rate-by-past-team" },
        { label: "View My Ratings", url: "/my-ratings" },
      ],
    },
  ];

  const chairpersonTabs = [
    {
      label: "List",
      url: "/",
      subtabs: [
        { label: "By Name", url: "/" },
        { label: "Check-In", url: "/checkin" },
        { label: "Cut", url: "/cut" },
        { label: "Archive", url: "/archive" },
      ],
    },
    {
      label: "Teams",
      url: "/teams",
      subtabs: [
        { label: "Teams", url: "/teams" },
        { label: "Finals Teams", url: "/finals-teams" },
      ],
    },
    { label: "Schedule", url: "/schedule" },
    {
      label: "Ratings",
      url: "/rate",
      subtabs: [
        { label: "Rate By Name", url: "/rate" },
        { label: "Rate By Current Team", url: "/rate-by-team" },
        { label: "Rate By Past Team", url: "/rate-by-past-team" },
        { label: "View Ratings", url: "/ratings" },
        { label: "View My Ratings", url: "/my-ratings" },
      ],
    },
    {
      label: "Analytics",
      url: "/schedule",
      subtabs: [
        { label: "Court", url: "/schedule" },
        { label: "Match", url: "/schedule" },
        { label: "Leaderboards", url: "/schedule" },
      ],
    },
  ];

  var tabs = [];
  switch (group) {
    case "ballkid":
      tabs = ballkidTabs;
      break;
    case "captain":
      tabs = captainTabs;
      break;
    case "chairperson":
      tabs = chairpersonTabs;
      break;
    default:
      break;
    // console.log("Unrecognized group: " + group);
  }

  return (
    // <Box sx={{ flexGrow: 1 }}>
    <AppBar position="static">
      <Toolbar>
        {/* <IconButton
              size="large"
              edge="start"
              color="inherit"
              sx={{ mr: 2 }}
            >
              <Menu />
            </IconButton> */}
        <div className="justify" style={{ height: "100%" }}>
          <div className="sxs">
            <div className="sxs">
              <Icon>
                <SportsTennis />
              </Icon>
              <Typography
                component={Link}
                to="/"
                variant="h6"
                sx={{ mx: 2, textDecoration: "none", color: "white" }}
                // sx={{ flexGrow: 1, textDecoration: "none", color: "white" }}
              >
                Citi Open Ballkids
              </Typography>
            </div>

            {!props.isLoggedIn ? (
              ""
            ) : (
              <div className="sxs">
                {tabs.map((tab) => (
                  <NavbarItem key={tab.label} tab={tab} />
                ))}
              </div>
            )}
          </div>

          {!props.isLoggedIn ? (
            <Button color="inherit" component={Link} to="/login">
              Login
            </Button>
          ) : (
            <Button
              color="inherit"
              component={Link}
              to="/login"
              onClick={() => {
                props.setToken("");
                setSessionStorage("group", "");
                setSessionStorage("ballkid_id", "");
                setSessionStorage("username", "");
              }}
            >
              Logout
            </Button>
          )}
        </div>
      </Toolbar>
    </AppBar>
    // </Box>
  );
}
