import React from "react";

import Typography from "@mui/material/Typography";
import Link from "@mui/material/Link";

export default function FeedbackPage() {
  return (
    <div className="page">
      <Typography variant="h4" sx={{ mb: 1 }}>
        Got Feedback?
      </Typography>

      <Typography>
        Got any feedback on the tournament, captains, website, etc.? We would
        love to hear it!
        <br /> <br />
        Submit anonymous feedback{" "}
        <Link target="_blank" href="https://forms.gle/J9BH4jC94RxWzMm79">
          here
        </Link>{" "}
        or feel free to email mubadalacitiopenballcrew@gmail.com.
      </Typography>
    </div>
  );
}
