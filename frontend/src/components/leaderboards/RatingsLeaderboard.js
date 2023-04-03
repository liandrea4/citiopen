import React, { useState, useEffect } from "react";
import { Typography, Link } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";

import { getAuthHeader } from "../Utils";
import { EventSeat } from "@mui/icons-material";

export default function RatingsLeaderboard(props) {
  const [leaderboard, setLeaderboard] = useState([]);

  useEffect(() => {
    fetch("/api/get-ratings-leaderboard", { headers: getAuthHeader() })
      .then((response) => response.json())
      .then((data) => setLeaderboard(data));
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
      headerName: "Captain / Chairperson",
      width: 200,
      renderCell: (rowData) => (
        <div className="sxs">
          <Link href={`/ballkid/${rowData.row.id}`}>
            {rowData.row.ballkidName}
          </Link>
          {rowData.row.isChairperson ? (
            <EventSeat sx={{ color: "purple", ml: 1 }} />
          ) : (
            ""
          )}
        </div>
      ),
    },
    {
      field: "numRatings",
      headerName: "# of Ratings",
      width: 100,
      valueGetter: (rowData) => rowData.row.numRatings,
    },
    {
      field: "avgRating",
      headerName: "Average",
      width: 150,
      valueGetter: (rowData) => rowData.row.avgRating,
      valueFormatter: (obj) => Number(obj.value.toFixed(3)),
    },
    {
      field: "stdevRating",
      headerName: "Standard Deviation",
      width: 150,
      valueGetter: (rowData) => rowData.row.stdevRating,
      valueFormatter: (obj) => Number(obj.value.toFixed(3)),
    },
    {
      field: "scale",
      headerName: "Calibration Scale",
      width: 150,
      valueGetter: (rowData) => rowData.row.scale,
      valueFormatter: (obj) => Number(obj.value.toFixed(3)),
    },
    {
      field: "offset",
      headerName: "Calibration Offset",
      width: 150,
      valueGetter: (rowData) => rowData.row.offset,
      valueFormatter: (obj) => Number(obj.value.toFixed(3)),
    },
  ];

  const rows = leaderboard.map((ballkid) => ({
    id: ballkid.id,
    ballkidName: ballkid.ballkid_name,
    isChairperson: ballkid.is_chairperson,
    numRatings: ballkid.num_ratings,
    avgRating: ballkid.avg_rating,
    stdevRating: ballkid.stdev_rating,
    scale: ballkid.scale,
    offset: ballkid.offset,
  }));

  return (
    <div className="page">
      <Typography variant="h4" sx={{ mb: 2 }}>
        Ratings Leaderboard
      </Typography>

      <div style={{ height: 500 }}>
        <DataGrid
          columns={columns}
          rows={rows}
          pageSize={25}
          density="compact"
        />
      </div>

      <Typography variant="body1" mt={2}>
        Note: Average is the average of all the ratings submitted (NOT received)
        by this captain/chairperson. Likewise for standard deviation.
        Calibration scale and offset are calculated for each rater by the
        calibration method described{" "}
        <Link
          target="_blank"
          href="https://github.com/jtiosue/rcal/blob/master/report/review_calibration.pdf"
        >
          here
        </Link>
        .
      </Typography>
    </div>
  );
}
