import React, { useState, useEffect } from "react";

import Typography from "@mui/material/Typography";
import Table from "@mui/material/Table";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableCell from "@mui/material/TableCell";
import TableRow from "@mui/material/TableRow";
import TableBody from "@mui/material/TableBody";
import CircularProgress from "@mui/material/CircularProgress";

import { DataGrid } from "@mui/x-data-grid";

import {
  getAuthHeader,
  getTimeStr,
  getTimeFloat,
  BallkidAndIcon,
  HelpIcon,
} from "../Utils";
import { Box } from "@mui/material";
import { checkinLeaderboard } from "../HelpMessages";

function renderAverages(averages) {
  return (
    <TableContainer sx={{ mt: 1, mb: 3 }}>
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell align="center"></TableCell>
            <TableCell align="center">Total Time</TableCell>
            <TableCell align="center"># of Days</TableCell>
            <TableCell align="center">Average Time Per Day</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          <TableRow>
            <TableCell align="center" width="22%">
              Average
            </TableCell>
            <TableCell align="center">
              {getTimeStr(parseFloat(averages["checkin_avg"]) / 3600)}
            </TableCell>
            <TableCell align="center">
              {Number(averages["days_avg"]).toFixed(1)}
            </TableCell>
            <TableCell align="center">
              {getTimeStr(
                parseFloat(averages["checkin_avg"] / averages["days_avg"]) /
                  3600
              )}
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </TableContainer>
  );
}

export default function CheckinLeaderboard(props) {
  const [ballkids, setBallkids] = useState([]);
  const [averages, setAverages] = useState();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/get-checkin-leaderboard", { headers: getAuthHeader() })
      .then((response) => response.json())
      .then((data) => setBallkids(data));

    fetch("/api/get-average-checkin-leaderboard", { headers: getAuthHeader() })
      .then((response) => response.json())
      .then((data) => setAverages(data))
      .then(() => setLoading(false));
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
      field: "time",
      headerName: "Total Time",
      width: 200,
      valueGetter: (rowData) => getTimeFloat(rowData.row.time),
      valueFormatter: (obj) => getTimeStr(obj.value),
    },
    {
      field: "days",
      headerName: "# of Days",
      width: 100,
      valueGetter: (rowData) => rowData.row.days,
    },
    {
      field: "timePerDay",
      headerName: "Average Time Per Day",
      width: 200,
      valueGetter: (rowData) =>
        getTimeFloat(rowData.row.time) / rowData.row.days,
      valueFormatter: (obj) => getTimeStr(obj.value),
    },
  ];

  const rows = ballkids.map((ballkid) => ({
    id: ballkid.id,
    ballkid: ballkid,
    days: ballkid.checkin_days,
    time: ballkid.checkin_duration,
  }));

  return (
    <div className="page">
      <Box className="sxs" sx={{ mb: 1 }}>
        <Typography variant="h4">Check-in Leaderboard</Typography>
        &thinsp;
        <HelpIcon page="Check-in Leaderboard" message={checkinLeaderboard} />
      </Box>

      {loading ? (
        <CircularProgress className="center" size={30} />
      ) : (
        <div>
          {averages !== undefined ? renderAverages(averages) : ""}

          <div style={{ height: 500 }}>
            <DataGrid
              columns={columns}
              rows={rows}
              pageSize={25}
              density="compact"
            />
          </div>
        </div>
      )}
    </div>
  );
}
