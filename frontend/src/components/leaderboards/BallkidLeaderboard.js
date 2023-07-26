import React, { useState, useEffect } from "react";

import Typography from "@mui/material/Typography";

import { DataGrid } from "@mui/x-data-grid";

import { BallkidAndIcon, HelpIcon, getAuthHeader } from "../Utils";
import { Box } from "@mui/material";
import { ratingsBallkidLeaderboard } from "../HelpMessages";

export default function BallkidLeaderboard(props) {
  const [ballkids, setBallkids] = useState([]);

  useEffect(() => {
    fetch("/api/get-ballkid-leaderboard", { headers: getAuthHeader() })
      .then((response) => response.json())
      .then((data) => setBallkids(data));
  }, []);

  const columns = [
    {
      field: "rank",
      headerName: "",
      width: 30,
      sortable: true,
      renderCell: (index) => index.api.getRowIndex(index.row.id) + 1,
    },
    {
      field: "name",
      headerName: "Ballkid",
      width: 200,
      renderCell: (rowData) => <BallkidAndIcon ballkid={rowData.row.ballkid} />,
    },
    {
      field: "numRatings",
      headerName: "# of Ratings",
      width: 100,
      valueGetter: (rowData) => rowData.row.ballkid.num_ratings,
    },

    {
      field: "avgRating",
      headerName: "Average",
      width: 150,
      valueGetter: (rowData) => rowData.row.ballkid.raw_avg,
      valueFormatter: (obj) => (!obj.value ? "" : Number(obj.value.toFixed(3))),
    },
    {
      field: "stdevRating",
      headerName: "Standard Deviation",
      width: 150,
      valueGetter: (rowData) => rowData.row.ballkid.raw_stdev,
      valueFormatter: (obj) => (!obj.value ? "" : Number(obj.value.toFixed(3))),
    },
    {
      field: "offset",
      headerName: "Calibrated Average",
      width: 150,
      valueGetter: (rowData) => rowData.row.ballkid.calibrated_avg,
      valueFormatter: (obj) => (!obj.value ? "" : Number(obj.value.toFixed(3))),
    },
    {
      field: "improvement",
      headerName: "Calibrated St. Dev.",
      width: 150,
      valueGetter: (rowData) => rowData.row.ballkid.calibrated_stdev,
      valueFormatter: (obj) => (!obj.value ? "" : Number(obj.value.toFixed(3))),
    },
  ];

  const rows = ballkids.map((ballkid) => ({
    id: ballkid.id,
    ballkid: ballkid,
  }));

  return (
    <div className="page">
      <Box className="sxs" sx={{ mb: 1 }}>
        <Typography variant="h4">Ratings Leaderboard - Ballkid</Typography>
        &thinsp;
        <HelpIcon
          page="Ratings Leaderboard - Ballkid"
          message={ratingsBallkidLeaderboard}
        />
      </Box>

      <div style={{ height: 500 }}>
        <DataGrid
          columns={columns}
          rows={rows}
          pageSize={25}
          density="compact"
        />
      </div>
    </div>
  );
}
