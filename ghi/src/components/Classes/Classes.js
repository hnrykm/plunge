import { React, useEffect, useState } from "react";
import { Carousel, Stack } from "react-bootstrap";

function UpcomingClasses() {
  const [classes, setClasses] = useState([]);
  const [classes1, setClasses1] = useState([]);
  const [classes2, setClasses2] = useState([]);

  const baseUrl = process.env.REACT_APP_API_HOST;

  useEffect(() => {
    async function loadClasses() {
      const response = await fetch(`${baseUrl}/api/classes?feed=upcoming`);
      if (response.ok) {
        const data = await response.json();
        setClasses(data);
      } else {
        console.error(response);
      }
    }
    loadClasses();
  }, []);

  useEffect(() => {
    function setStack() {
      setClasses1(classes.slice(0, 4));
    }
    setStack();
  }, [classes]);

  useEffect(() => {
    function setStack() {
      setClasses2(classes.slice(4, 8));
    }
    setStack();
  }, [classes]);

  return (
    <div className="upcoming-container">
      <h1 className="upcoming-title">Upcoming</h1>
      <a href="/all-upcoming" className="more-classes-btn">
        <button
          type="button"
          className="btn btn-outline-primary more-classes-btn"
        >
          See More...
        </button>
      </a>
      <Carousel variant="dark" className="upcoming-carousel">
        <Carousel.Item>
          <Stack className="card-stack" direction="horizontal" gap={3}>
            {classes1.map((classIterable, Idx) => {
              const classDetailUrl = `classes/${classIterable.id}`;
              return (
                <div className="card location-card mx-2" key={Idx}>
                  <div className="card-body location-card">
                    <img
                      src={classIterable.image_1}
                      className="card-img-top"
                      alt="..."
                    />
                    <h5 className="card-title location-card">
                      {classIterable.class_name}
                    </h5>
                    <div></div>
                    <p className="card-text location-card">
                      {classIterable.description.length > 143
                        ? classIterable.description.substr(0, 140) + "..."
                        : classIterable.description}
                    </p>
                    <ul className="list-group list-group-flush location-card">
                      <li className="list-group-item">
                        <p className="card-text location-card">
                          {classIterable.location_address.length > 16
                            ? classIterable.location_address.substr(0, 13) +
                              "..."
                            : classIterable.location_address}
                        </p>
                      </li>
                      <li className="list-group-item">
                        <a href={classDetailUrl} className="btn btn-primary">
                          Class Details
                        </a>
                      </li>
                    </ul>
                  </div>
                </div>
              );
            })}
          </Stack>
        </Carousel.Item>
        <Carousel.Item>
          <Stack className="card-stack" direction="horizontal" gap={3}>
            {classes2.map((classIterable, Idx) => {
              const classDetailUrl = `classes/${classIterable.id}`;
              return (
                <div className="card location-card mx-2" key={Idx}>
                  <div className="card-body location-card">
                    <img
                      src={classIterable.image_1}
                      className="card-img-top"
                      alt="..."
                    />
                    <h5 className="card-title location-card">
                      {classIterable.class_name}
                    </h5>
                    <p className="card-text location-card">
                      {classIterable.description.length > 153
                        ? classIterable.description.substr(0, 150) + "..."
                        : classIterable.description}
                    </p>
                    <ul className="list-group list-group-flush location-card">
                      <li className="list-group-item">
                        <p className="card-text location-card">
                          {classIterable.location_address.length > 18
                            ? classIterable.location_address.substr(0, 15) +
                              "..."
                            : classIterable.location_address}
                        </p>
                      </li>
                      <li className="list-group-item">
                        <a href={classDetailUrl} className="btn btn-primary">
                          Class Details
                        </a>
                      </li>
                    </ul>
                  </div>
                </div>
              );
            })}
          </Stack>
        </Carousel.Item>
      </Carousel>
    </div>
  );
}

export default UpcomingClasses;
