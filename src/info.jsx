import React from "react";
import { InfoBox } from "@react-google-maps/api";
import { Card, Button } from "react-bootstrap";
function Info(props) {
  return (
    <InfoBox position={{ lat: props.latitude, lng: props.longitude }}>
      <Card style={{ width: "18rem" }}>
        <Card.Body>
          <Card.Title size="md">Restaurant</Card.Title>
          <Card.Text>Bullshit</Card.Text>
          <Button variant="primary" size="sm" onClick={addReview}>
            Add Review
          </Button>
        </Card.Body>
      </Card>
    </InfoBox>
  );
}

export default Info;
