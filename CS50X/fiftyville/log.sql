-- Keep a log of any SQL queries you execute as you solve the mystery.
-- Problem:
--      Who the thief is,
--      What city the thief escaped to, and
--      Who the thief’s accomplice is who helped them escape

--      All you know is that the theft took place on July 28, 2021 and that it took place on Humphrey Street.

-- Log:
-- Following the recommended start of the problem set, I can find the description of the crime
-- with good data to search for next

SELECT description
FROM crime_scene_reports
WHERE year = 2021
AND month = 7
AND day = 28;

-- The description of CS50 Theft:
--      Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery.
--      Interviews were conducted today with three witnesses who were present at the time –
--      each of their interview transcripts mentions the bakery.

-- Useful info:
--      10:15am
--      Humphrey Street Bakery
--      Interviews with 3 Witnesses

-- Should read the interviews for more useful information

SELECT name,transcript
FROM interviews
WHERE year = 2021
AND month = 7
AND day = 28;

-- According to the contents this 3 should be the correct interviews
-- interviews should have been linked to crime reports

-- Ruth:
--      Sometime within ten minutes of the theft,
--      I saw the thief get into a car in the bakery parking lot and drive away.
--      If you have security footage from the bakery parking lot, you might want
--      to look for cars that left the parking lot in that time frame.                                                          |
-- Eugene:
--      I don't know the thief's name, but it was someone I recognized.
--      Earlier this morning, before I arrived at Emma's bakery,
--      I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.                                                                                                 |
-- Raymond:
--      As the thief was leaving the bakery, they called someone who talked to them
--      for less than a minute. In the call, I heard the thief say that they were
--      planning to take the earliest flight out of Fiftyville tomorrow.
--      The thief then asked the person on the other end of the phone to purchase the flight ticket.

-- Update to Useful Info:

--      Current Timeline:

--          Date 28/07/2021
--          Spotted: ~05:00am : ~10:00am - ATM on Leggett Street, withdrawing money
--          Theft:    10:15am            - Humphrey Street Bakery
--          Call:    ~10:15am : ~10:16am - Call for less then 1 minute
--          Getaway: ~10:15am : ~10:25am - Bakery Parking lot
--          Ticket:  ~28/07/2021         - Possibly bought today

--          Date 29/07/2021
--          Earliest Flight available

--      Other info:
--      Bakery is owned by Emma
--      Interviewed were named Ruth, Eugene, Raymond

-- Could probably check what flights are available

SELECT *
FROM flights
WHERE year = 2021
AND month = 7
AND day = 29
AND origin_airport_id =
    (
        SELECT id
        FROM airports
        WHERE city LIKE "Fiftyville"
    )
ORDER BY hour ASC, minute ASC
;

-- New info:
--      Earliest flight leaving from fiftyville,
--      Date 29/07/2021 08:20
--      Destination airport ID: 4

-- Need to find out airport by the ID 4

SELECT *
FROM airports
WHERE id = 4;

-- Target Airport:
--       ID:   4
--       Abbr: LGA
--       Name: LaGuardia Airport
--       City: New York City

-- Still need to check security for bakery, phone calls, atm withdraws

-- Going to try and analyse bakery security
-- Getaway: ~10:15am : ~10:25am - Bakery Parking lot
-- Interviewee said around 10 mins mark

SELECT *
FROM bakery_security_logs
WHERE year = 2021
AND month = 7
AND day = 28
AND hour = 10
AND minute > 14
AND minute < 30;

--| id  | year | month | day | hour | minute | activity | license_plate
--| 260 | 2021 | 7     | 28  | 10   | 16     | exit     | 5P2BI95       |
--| 261 | 2021 | 7     | 28  | 10   | 18     | exit     | 94KL13X       |
--| 262 | 2021 | 7     | 28  | 10   | 18     | exit     | 6P58WS2       |
--| 263 | 2021 | 7     | 28  | 10   | 19     | exit     | 4328GD8       |
--| 264 | 2021 | 7     | 28  | 10   | 20     | exit     | G412CB7       | LIKELY
--| 265 | 2021 | 7     | 28  | 10   | 21     | exit     | L93JTIZ       | LIKELY
--| 266 | 2021 | 7     | 28  | 10   | 23     | exit     | 322W7JE       | MORE LIKELY
--| 267 | 2021 | 7     | 28  | 10   | 23     | exit     | 0NTHK55       | MORE LIKELY

-- Could find out the calls on that day with less then 1 minute duration to try
-- and find a common link between the license plate and phone numbers
-- Call:    ~10:15am : ~10:16am - Call for less then 1 minute

SELECT * FROM phone_calls
WHERE year = 2021
AND month = 7
AND day = 28
AND duration < 61;

--| id  |     caller     |    receiver    | year | month | day | duration |
--| 221 | (130) 555-0289 | (996) 555-8899 | 2021 | 7     | 28  | 51       |
--| 224 | (499) 555-9472 | (892) 555-8872 | 2021 | 7     | 28  | 36       |
--| 233 | (367) 555-5533 | (375) 555-8161 | 2021 | 7     | 28  | 45       |
--| 234 | (609) 555-5876 | (389) 555-5198 | 2021 | 7     | 28  | 60       |
--| 251 | (499) 555-9472 | (717) 555-1342 | 2021 | 7     | 28  | 50       |
--| 254 | (286) 555-6063 | (676) 555-6554 | 2021 | 7     | 28  | 43       |
--| 255 | (770) 555-1861 | (725) 555-3243 | 2021 | 7     | 28  | 49       |
--| 261 | (031) 555-6622 | (910) 555-3251 | 2021 | 7     | 28  | 38       |
--| 279 | (826) 555-1652 | (066) 555-9701 | 2021 | 7     | 28  | 55       |
--| 281 | (338) 555-6650 | (704) 555-2131 | 2021 | 7     | 28  | 54       |

-- Could try and correlate now the caller number with license plates found in
-- the bakery parking lot

SELECT *
FROM people
WHERE phone_number IN
    (
        SELECT caller FROM phone_calls
        WHERE year = 2021
        AND month = 7
        AND day = 28
        AND duration < 61
    )
AND license_plate IN
    (
        SELECT license_plate
        FROM bakery_security_logs
        WHERE year = 2021
        AND month = 7
        AND day = 28
        AND hour = 10
        AND minute > 14
        AND minute < 30
    )
;

-- According to the timeline of the witness I can attribute different weights to each - Main Thief

--|   id   |  name  |  phone_number  | passport_number | license_plate |
--| 398010 | Sofia  | (130) 555-0289 | 1695452385      | G412CB7       | 10:20 LIKELY
--| 514354 | Diana  | (770) 555-1861 | 3592750733      | 322W7JE       | 10:23 MORE LIKELY
--| 560886 | Kelsey | (499) 555-9472 | 8294398571      | 0NTHK55       | 10:23 MORE LIKELY
--| 686048 | Bruce  | (367) 555-5533 | 5773159633      | 94KL13X       | 10:18 LESS LIKELY


-- Now i can also check what people were callled by this suspects on that day

SELECT * FROM phone_calls
WHERE year = 2021
AND month = 7
AND day = 28
AND duration < 61
AND caller IN
    (
        SELECT phone_number
        FROM people
        WHERE phone_number IN
            (
                SELECT caller FROM phone_calls
                WHERE year = 2021
                AND month = 7
                AND day = 28
                AND duration < 61
            )
        AND license_plate IN
            (
                SELECT license_plate
                FROM bakery_security_logs
                WHERE year = 2021
                AND month = 7
                AND day = 28
                AND hour = 10
                AND minute > 14
                AND minute < 30
            )
    )
;

--| id  |     caller     |    receiver    | year | month | day | duration |
--| 221 | (130) 555-0289 | (996) 555-8899 | 2021 | 7     | 28  | 51       |
--| 224 | (499) 555-9472 | (892) 555-8872 | 2021 | 7     | 28  | 36       |
--| 233 | (367) 555-5533 | (375) 555-8161 | 2021 | 7     | 28  | 45       |
--| 251 | (499) 555-9472 | (717) 555-1342 | 2021 | 7     | 28  | 50       |
--| 255 | (770) 555-1861 | (725) 555-3243 | 2021 | 7     | 28  | 49       |

-- Now i can cross check the receiver phone numbers with people to get a list of suspects of being accomplice

SELECT *
FROM people
WHERE phone_number IN
    (
        SELECT receiver FROM phone_calls
        WHERE year = 2021
        AND month = 7
        AND day = 28
        AND duration < 61
        AND caller IN
            (
                SELECT phone_number
                FROM people
                WHERE phone_number IN
                    (
                        SELECT caller FROM phone_calls
                        WHERE year = 2021
                        AND month = 7
                        AND day = 28
                        AND duration < 61
                    )
                AND license_plate IN
                    (
                        SELECT license_plate
                        FROM bakery_security_logs
                        WHERE year = 2021
                        AND month = 7
                        AND day = 28
                        AND hour = 10
                        AND minute > 14
                        AND minute < 30
                    )
            )
    )
;

-- These were the people called by the main suspects, so the accomplice suspects

--|   id   |  name   |  phone_number  | passport_number | license_plate |
--| 251693 | Larry   | (892) 555-8872 | 2312901747      | O268ZZ0       |
--| 567218 | Jack    | (996) 555-8899 | 9029462229      | 52R0Y8U       |
--| 626361 | Melissa | (717) 555-1342 | 7834357192      |               |
--| 847116 | Philip  | (725) 555-3243 | 3391710505      | GW362R6       |
--| 864400 | Robin   | (375) 555-8161 |                 | 4V16VO0       |


-- Situation report:

-- I have a list of suspects of the robbing the  bakery, and also a list
-- of people who were called on that day from the suspects.

-- I haven't checked the withdraws, could probably correlate the withdraws with the suspect list and reduce it,
-- also reducing the number of accomplices, (Insert "fuck" witcher meme here).

-- Then after reducing the suspect and accomplice list, I can also check who bought the tickets

-- Sitrep end.


-- Searching for atm withdraws, cross checking it with the main suspects
--      Date 28/07/2021
--      Spotted: ~05:00am : ~10:00am - ATM on Leggett Street, withdrawing money


SELECT atm_transactions.*
FROM atm_transactions,bank_accounts
WHERE atm_transactions.account_number = bank_accounts.account_number
AND bank_accounts.person_id IN
    (
        SELECT id
        FROM people
        WHERE phone_number IN
            (
                SELECT caller FROM phone_calls
                WHERE year = 2021
                AND month = 7
                AND day = 28
                AND duration < 61
            )
        AND license_plate IN
            (
                SELECT license_plate
                FROM bakery_security_logs
                WHERE year = 2021
                AND month = 7
                AND day = 28
                AND hour = 10
                AND minute > 14
                AND minute < 30
            )
    )
AND atm_transactions.year = 2021
AND atm_transactions.month = 7
AND atm_transactions.day = 28
AND atm_transactions.atm_location LIKE "Leggett Street"
;

-- The result

-- | id  | account_number | year | month | day |  atm_location  | transaction_type | amount |
-- | 267 | 49610011       | 2021 | 7     | 28  | Leggett Street | withdraw         | 50     |
-- | 336 | 26013199       | 2021 | 7     | 28  | Leggett Street | withdraw         | 35     |

-- Need to crosscheck account numbers with people, to find out the new suspects

SELECT people.*
FROM people,bank_accounts
WHERE phone_number IN
    (
        SELECT caller FROM phone_calls
        WHERE year = 2021
        AND month = 7
        AND day = 28
        AND duration < 61
    )
AND license_plate IN
    (
        SELECT license_plate
        FROM bakery_security_logs
        WHERE year = 2021
        AND month = 7
        AND day = 28
        AND hour = 10
        AND minute > 14
        AND minute < 30
    )
AND bank_accounts.person_id = people.id
AND bank_accounts.account_number IN
    (
        SELECT atm_transactions.account_number
        FROM atm_transactions,bank_accounts
        WHERE atm_transactions.account_number = bank_accounts.account_number
        AND bank_accounts.person_id IN
            (
                SELECT id
                FROM people
                WHERE phone_number IN
                    (
                        SELECT caller FROM phone_calls
                        WHERE year = 2021
                        AND month = 7
                        AND day = 28
                        AND duration < 61
                    )
                AND license_plate IN
                    (
                        SELECT license_plate
                        FROM bakery_security_logs
                        WHERE year = 2021
                        AND month = 7
                        AND day = 28
                        AND hour = 10
                        AND minute > 14
                        AND minute < 30
                    )
            )
        AND atm_transactions.year = 2021
        AND atm_transactions.month = 7
        AND atm_transactions.day = 28
        AND atm_transactions.atm_location LIKE "Leggett Street"
    )
;

-- Main Suspects

--|   id   | name  |  phone_number  | passport_number | license_plate |
--| 686048 | Bruce | (367) 555-5533 | 5773159633      | 94KL13X       |
--| 514354 | Diana | (770) 555-1861 | 3592750733      | 322W7JE       |

-- Getaway: ~10:15am : ~10:25am - Bakery Parking lot
-- Interviewee said around 10 mins mark

-- Checking the info i got before Bruce left at 10:18
-- and Diana left at 10:23

-- Which puts more weight in Diana as the main Thief,
-- now to check the accomplice list

-- This gives me number the potential thieves called

SELECT * FROM phone_calls
WHERE year = 2021
AND month = 7
AND day = 28
AND duration < 61
AND caller IN
    (
        SELECT people.phone_number
        FROM people,bank_accounts
        WHERE phone_number IN
            (
                SELECT caller FROM phone_calls
                WHERE year = 2021
                AND month = 7
                AND day = 28
                AND duration < 61
            )
        AND license_plate IN
            (
                SELECT license_plate
                FROM bakery_security_logs
                WHERE year = 2021
                AND month = 7
                AND day = 28
                AND hour = 10
                AND minute > 14
                AND minute < 30
            )
        AND bank_accounts.person_id = people.id
        AND bank_accounts.account_number IN
            (
                SELECT atm_transactions.account_number
                FROM atm_transactions,bank_accounts
                WHERE atm_transactions.account_number = bank_accounts.account_number
                AND bank_accounts.person_id IN
                    (
                        SELECT id
                        FROM people
                        WHERE phone_number IN
                            (
                                SELECT caller FROM phone_calls
                                WHERE year = 2021
                                AND month = 7
                                AND day = 28
                                AND duration < 61
                            )
                        AND license_plate IN
                            (
                                SELECT license_plate
                                FROM bakery_security_logs
                                WHERE year = 2021
                                AND month = 7
                                AND day = 28
                                AND hour = 10
                                AND minute > 14
                                AND minute < 30
                            )
                    )
                AND atm_transactions.year = 2021
                AND atm_transactions.month = 7
                AND atm_transactions.day = 28
                AND atm_transactions.atm_location LIKE "Leggett Street"
            )
    )
;

--| id  |     caller     |    receiver    | year | month | day | duration |
--| 233 | (367) 555-5533 | (375) 555-8161 | 2021 | 7     | 28  | 45       |
--| 255 | (770) 555-1861 | (725) 555-3243 | 2021 | 7     | 28  | 49       |

-- Now to find out the accomplices

SELECT *
FROM people
WHERE phone_number IN
    (
        SELECT receiver FROM phone_calls
        WHERE year = 2021
        AND month = 7
        AND day = 28
        AND duration < 61
        AND caller IN
            (
                SELECT people.phone_number
                FROM people,bank_accounts
                WHERE phone_number IN
                    (
                        SELECT caller FROM phone_calls
                        WHERE year = 2021
                        AND month = 7
                        AND day = 28
                        AND duration < 61
                    )
                AND license_plate IN
                    (
                        SELECT license_plate
                        FROM bakery_security_logs
                        WHERE year = 2021
                        AND month = 7
                        AND day = 28
                        AND hour = 10
                        AND minute > 14
                        AND minute < 30
                    )
                AND bank_accounts.person_id = people.id
                AND bank_accounts.account_number IN
                    (
                        SELECT atm_transactions.account_number
                        FROM atm_transactions,bank_accounts
                        WHERE atm_transactions.account_number = bank_accounts.account_number
                        AND bank_accounts.person_id IN
                            (
                                SELECT id
                                FROM people
                                WHERE phone_number IN
                                    (
                                        SELECT caller FROM phone_calls
                                        WHERE year = 2021
                                        AND month = 7
                                        AND day = 28
                                        AND duration < 61
                                    )
                                AND license_plate IN
                                    (
                                        SELECT license_plate
                                        FROM bakery_security_logs
                                        WHERE year = 2021
                                        AND month = 7
                                        AND day = 28
                                        AND hour = 10
                                        AND minute > 14
                                        AND minute < 30
                                    )
                            )
                        AND atm_transactions.year = 2021
                        AND atm_transactions.month = 7
                        AND atm_transactions.day = 28
                        AND atm_transactions.atm_location LIKE "Leggett Street"
                    )
            )
    )
;

-- The accomplice suspects

--|   id   |  name  |  phone_number  | passport_number | license_plate |
--| 847116 | Philip | (725) 555-3243 | 3391710505      | GW362R6       |
--| 864400 | Robin  | (375) 555-8161 |                 | 4V16VO0       |

-- Main Suspects

--|   id   | name  |  phone_number  | passport_number | license_plate |
--| 686048 | Bruce | (367) 555-5533 | 5773159633      | 94KL13X       |
--| 514354 | Diana | (770) 555-1861 | 3592750733      | 322W7JE       | More likely due to parking time

-- Flight info:
--      Ticket:  ~28/07/2021         - Possibly bought today
--
--      Earliest flight leaving from fiftyville,
--      Date 29/07/2021 08:20
--      Destination airport ID: 4
--
--      Target Airport:
--              ID:   4
--              Abbr: LGA
--              Name: LaGuardia Airport
--              City: New York City

-- Now I need to cross reference the tickets bought by the possible accomplices
-- and cross reference the passengers in the earliest flight with the thief


-- Realization:
--      After analysing the tables properly, there's no way to find out who bought the ticket
--      So only when checking the smallest list of suspects against the flight,
--      it should return just 1 accomplice, but still, he should be on the small list from before or
--      something went wrong.

-- Cross checking the list of smallest suspects against the earliest flight I found earlier


SELECT passengers.*
FROM passengers, flights, people
WHERE passengers.flight_id = flights.id
AND passengers.passport_number = people.passport_number
AND flights.id IN
    (
        SELECT id
        FROM flights
        WHERE year = 2021
        AND month = 7
        AND day = 29
        AND origin_airport_id =
            (
                SELECT id
                FROM airports
                WHERE city LIKE "Fiftyville"
            )
        AND hour = 8
        AND minute = 20
        AND destination_airport_id = 4
    )
AND passengers.passport_number IN
    (
        SELECT people.passport_number
        FROM people,bank_accounts
        WHERE phone_number IN
            (
                SELECT caller FROM phone_calls
                WHERE year = 2021
                AND month = 7
                AND day = 28
                AND duration < 61
            )
        AND license_plate IN
            (
                SELECT license_plate
                FROM bakery_security_logs
                WHERE year = 2021
                AND month = 7
                AND day = 28
                AND hour = 10
                AND minute > 14
                AND minute < 30
            )
        AND bank_accounts.person_id = people.id
        AND bank_accounts.account_number IN
            (
                SELECT atm_transactions.account_number
                FROM atm_transactions,bank_accounts
                WHERE atm_transactions.account_number = bank_accounts.account_number
                AND bank_accounts.person_id IN
                    (
                        SELECT id
                        FROM people
                        WHERE phone_number IN
                            (
                                SELECT caller FROM phone_calls
                                WHERE year = 2021
                                AND month = 7
                                AND day = 28
                                AND duration < 61
                            )
                        AND license_plate IN
                            (
                                SELECT license_plate
                                FROM bakery_security_logs
                                WHERE year = 2021
                                AND month = 7
                                AND day = 28
                                AND hour = 10
                                AND minute > 14
                                AND minute < 30
                            )
                    )
                AND atm_transactions.year = 2021
                AND atm_transactions.month = 7
                AND atm_transactions.day = 28
                AND atm_transactions.atm_location LIKE "Leggett Street"
            )
    )
;

--| flight_id | passport_number | seat |
--| 36        | 5773159633      | 4A   |

-- Need to check it against the peoples table

SELECT *
FROM people
WHERE passport_number IN
    (
        SELECT passengers.passport_number
        FROM passengers, flights, people
        WHERE passengers.flight_id = flights.id
        AND passengers.passport_number = people.passport_number
        AND flights.id IN
            (
                SELECT id
                FROM flights
                WHERE year = 2021
                AND month = 7
                AND day = 29
                AND origin_airport_id =
                    (
                        SELECT id
                        FROM airports
                        WHERE city LIKE "Fiftyville"
                    )
                AND hour = 8
                AND minute = 20
                AND destination_airport_id = 4
            )
        AND passengers.passport_number IN
            (
                SELECT people.passport_number
                FROM people,bank_accounts
                WHERE phone_number IN
                    (
                        SELECT caller FROM phone_calls
                        WHERE year = 2021
                        AND month = 7
                        AND day = 28
                        AND duration < 61
                    )
                AND license_plate IN
                    (
                        SELECT license_plate
                        FROM bakery_security_logs
                        WHERE year = 2021
                        AND month = 7
                        AND day = 28
                        AND hour = 10
                        AND minute > 14
                        AND minute < 30
                    )
                AND bank_accounts.person_id = people.id
                AND bank_accounts.account_number IN
                    (
                        SELECT atm_transactions.account_number
                        FROM atm_transactions,bank_accounts
                        WHERE atm_transactions.account_number = bank_accounts.account_number
                        AND bank_accounts.person_id IN
                            (
                                SELECT id
                                FROM people
                                WHERE phone_number IN
                                    (
                                        SELECT caller FROM phone_calls
                                        WHERE year = 2021
                                        AND month = 7
                                        AND day = 28
                                        AND duration < 61
                                    )
                                AND license_plate IN
                                    (
                                        SELECT license_plate
                                        FROM bakery_security_logs
                                        WHERE year = 2021
                                        AND month = 7
                                        AND day = 28
                                        AND hour = 10
                                        AND minute > 14
                                        AND minute < 30
                                    )
                            )
                        AND atm_transactions.year = 2021
                        AND atm_transactions.month = 7
                        AND atm_transactions.day = 28
                        AND atm_transactions.atm_location LIKE "Leggett Street"
                    )
            )
    )
;

--|   id   | name  |  phone_number  | passport_number | license_plate |
--| 686048 | Bruce | (367) 555-5533 | 5773159633      | 94KL13X       |

-- So it was Bruce all along, now check who bruce called in the day of the robbery, and we get the accomplice

-- Now reusing the same queries, I used to get the accomplices lists, I can get the person who was called by the thief

SELECT *
FROM people
WHERE phone_number IN
    (
        SELECT receiver FROM phone_calls
        WHERE year = 2021
        AND month = 7
        AND day = 28
        AND duration < 61
        AND caller IN
            (
                SELECT people.phone_number
                FROM people
                WHERE passport_number IN
                    (
                        SELECT passengers.passport_number
                        FROM passengers, flights, people
                        WHERE passengers.flight_id = flights.id
                        AND passengers.passport_number = people.passport_number
                        AND flights.id IN
                            (
                                SELECT id
                                FROM flights
                                WHERE year = 2021
                                AND month = 7
                                AND day = 29
                                AND origin_airport_id =
                                    (
                                        SELECT id
                                        FROM airports
                                        WHERE city LIKE "Fiftyville"
                                    )
                                AND hour = 8
                                AND minute = 20
                                AND destination_airport_id = 4
                            )
                        AND passengers.passport_number IN
                            (
                                SELECT people.passport_number
                                FROM people,bank_accounts
                                WHERE phone_number IN
                                    (
                                        SELECT caller FROM phone_calls
                                        WHERE year = 2021
                                        AND month = 7
                                        AND day = 28
                                        AND duration < 61
                                    )
                                AND license_plate IN
                                    (
                                        SELECT license_plate
                                        FROM bakery_security_logs
                                        WHERE year = 2021
                                        AND month = 7
                                        AND day = 28
                                        AND hour = 10
                                        AND minute > 14
                                        AND minute < 30
                                    )
                                AND bank_accounts.person_id = people.id
                                AND bank_accounts.account_number IN
                                    (
                                        SELECT atm_transactions.account_number
                                        FROM atm_transactions,bank_accounts
                                        WHERE atm_transactions.account_number = bank_accounts.account_number
                                        AND bank_accounts.person_id IN
                                            (
                                                SELECT id
                                                FROM people
                                                WHERE phone_number IN
                                                    (
                                                        SELECT caller FROM phone_calls
                                                        WHERE year = 2021
                                                        AND month = 7
                                                        AND day = 28
                                                        AND duration < 61
                                                    )
                                                AND license_plate IN
                                                    (
                                                        SELECT license_plate
                                                        FROM bakery_security_logs
                                                        WHERE year = 2021
                                                        AND month = 7
                                                        AND day = 28
                                                        AND hour = 10
                                                        AND minute > 14
                                                        AND minute < 30
                                                    )
                                            )
                                        AND atm_transactions.year = 2021
                                        AND atm_transactions.month = 7
                                        AND atm_transactions.day = 28
                                        AND atm_transactions.atm_location LIKE "Leggett Street"
                                    )
                            )
                    )
            )
    )
;

--|   id   | name  |  phone_number  | passport_number | license_plate |
--| 864400 | Robin | (375) 555-8161 |                 | 4V16VO0       |

-- It was Robin.

-- So the thief was Bruce, aided by Robin, and fled to New York City.

