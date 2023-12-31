from pydantic import BaseModel
from typing import List, Optional, Union
from datetime import datetime
from queries.pool import pool


class Error(BaseModel):
    message: str


class ReservationIn(BaseModel):
    event_id: int
    class_id: int
    # student_id: int
    total_price: float
    status: bool


class ReservationOut(BaseModel):
    id: int
    event_id: int
    class_id: int
    student_id: int
    total_price: float
    status: bool


class ReservationDetailsOut(BaseModel):
    id: int
    date_time: datetime
    capacity: int
    class_name: str
    instructor_id: int
    student_id: int
    student_first_name: str
    student_last_name: str
    location_name: str
    address: str
    city: str
    state: str
    zip_code: int
    total_price: float
    status: bool
    class_id: int
    event_id: int
    avatar: str


class ReservationStatusIn(BaseModel):
    status: bool


class ReservationStatusOut(BaseModel):
    id: int
    status: bool


class ReservationQuery:
    def get_one(self, reservation_id: int) -> Optional[ReservationDetailsOut]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        SELECT reservations.id
                            , events.date_time
                            , events.capacity
                            , classes.class_name
                            , classes.instructor_id
                            , reservations.student_id
                            , accounts.first_name
                            , accounts.last_name
                            , locations.name
                            , locations.address
                            , locations.city
                            , locations.state
                            , locations.zip_code
                            , total_price
                            , status
                            , classes.id
                            , events.id
                            , account_details.avatar
                        FROM reservations
                        INNER JOIN events ON reservations.event_id = events.id
                        INNER JOIN classes ON reservations.class_id = classes.id
                        INNER JOIN accounts ON reservations.student_id = accounts.id
                        INNER JOIN locations ON classes.location_id = locations.id
                        INNER JOIN account_details ON account_details.id = reservations.student_id
                        WHERE reservations.id = %s
                        """,
                        [reservation_id],
                    )
                    record = result.fetchone()
                    if record is None:
                        return None
                    return self.record_to_reservation_details_out(record)
        except Exception as e:
            print(e)
            return {"message": "Could not get that reservation"}

    def get_student(
        self, student_id: int
    ) -> Union[List[ReservationDetailsOut], Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        SELECT reservations.id
                            , events.date_time
                            , events.capacity
                            , classes.class_name
                            , classes.instructor_id
                            , reservations.student_id
                            , accounts.first_name
                            , accounts.last_name
                            , locations.name
                            , locations.address
                            , locations.city
                            , locations.state
                            , locations.zip_code
                            , total_price
                            , status
                            , classes.id
                            , events.id
                            , account_details.avatar
                        FROM reservations
                        INNER JOIN events ON reservations.event_id = events.id
                        INNER JOIN classes ON reservations.class_id = classes.id
                        INNER JOIN accounts ON reservations.student_id = accounts.id
                        INNER JOIN locations ON classes.location_id = locations.id
                        INNER JOIN account_details ON account_details.id = reservations.student_id
                        WHERE student_id = %s
                        order by events.date_time asc;
                        """,
                        [student_id],
                    )
                    return [
                        self.record_to_reservation_details_out(record)
                        for record in result
                    ]
        except Exception as e:
            print(e)
            return {"message": "Could not get reservations for that student"}

    def get_reservations_by_instructor(
        self, instructor_id: int
    ) -> Union[List[ReservationDetailsOut], Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        SELECT reservations.id
                            , events.date_time
                            , events.capacity
                            , classes.class_name
                            , classes.instructor_id
                            , reservations.student_id
                            , accounts.first_name
                            , accounts.last_name
                            , locations.name
                            , locations.address
                            , locations.city
                            , locations.state
                            , locations.zip_code
                            , total_price
                            , status
                            , classes.id
                            , events.id
                            , account_details.avatar
                        FROM reservations
                        INNER JOIN events ON reservations.event_id = events.id
                        INNER JOIN classes ON reservations.class_id = classes.id
                        INNER JOIN accounts ON reservations.student_id = accounts.id
                        INNER JOIN locations ON classes.location_id = locations.id
                        INNER JOIN account_details ON account_details.id = reservations.student_id
                        WHERE classes.instructor_id = %s;
                        """,
                        [instructor_id],
                    )
                    return [
                        self.record_to_reservation_details_out(record)
                        for record in result
                    ]
        except Exception as e:
            print(e)
            return {"message": "Could not get that reservation"}

    def update(
        self, reservation_id: int, reservation: ReservationStatusIn
    ) -> Union[ReservationStatusOut, Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    db.execute(
                        """
                        UPDATE reservations
                        SET status = %s
                        WHERE id = %s
                        """,
                        [
                            reservation.status,
                            reservation_id,
                        ],
                    )
                    return self.reservation_status_in_to_out(
                        reservation_id, reservation
                    )
        except Exception as e:
            print(e)
            return {"message": "Could not update that reservation"}

    def create(
        self, account_id, reservation: ReservationIn
    ) -> Union[ReservationOut, Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        INSERT INTO reservations
                            (event_id, class_id, student_id, total_price, status)
                        VALUES
                            (%s, %s, %s, %s, %s)
                        RETURNING id, student_id;
                        """,
                        [
                            reservation.event_id,
                            reservation.class_id,
                            account_id,
                            reservation.total_price,
                            reservation.status,
                        ],
                    )
                    response = result.fetchone()
                    id = response[0]
                    student_id = response[1]
                    return self.reservation_in_to_out(
                        id, student_id, reservation
                    )
        except Exception:
            return {"message": "Create did not work"}

    def reservation_status_in_to_out(
        self, id: int, reservation: ReservationStatusIn
    ):
        old_data = reservation.dict()
        return ReservationStatusOut(id=id, **old_data)

    def reservation_in_to_out(
        self, id, student_id, reservation: ReservationIn
    ):
        old_data = reservation.dict()
        return ReservationOut(id=id, student_id=student_id, **old_data)

    def record_to_reservation_out(self, record):
        return ReservationOut(
            id=record[0],
            event_id=record[1],
            class_id=record[2],
            student_id=record[3],
            total_price=record[4],
            status=record[5],
        )

    def record_to_reservation_details_out(self, record):
        return ReservationDetailsOut(
            id=record[0],
            date_time=record[1],
            capacity=record[2],
            class_name=record[3],
            instructor_id=record[4],
            student_id=record[5],
            student_first_name=record[6],
            student_last_name=record[7],
            location_name=record[8],
            address=record[9],
            city=record[10],
            state=record[11],
            zip_code=record[12],
            total_price=record[13],
            status=record[14],
            class_id=record[15],
            event_id=record[16],
            avatar=record[17],
        )
