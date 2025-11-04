from faker import Faker
import bson
from bsonstream import BSONInput

fake = Faker()

if __name__ == "__main__":
    print("generate 5000 fake profiles, write them all into a bson object,"
          "read back only those with @gmail.com emails")


    with open("fake_profiles.bson", "wb") as f:
        for _ in range(500):
            faked = fake.simple_profile()
            del faked['birthdate']  # bson doesn't like date wants datetime
            bson_data = bson.encode(faked)
            f.write(bson_data)

    found_gmails = 0
    with open("fake_profiles.bson", "rb") as f:
        stream = BSONInput(fh=f, fast_string_prematch=b"@gmail.com")
        for doc in stream:
            assert "@gmail" in doc['mail']  # bson handles the utf8 decoding by default!
            found_gmails += 1


    assert found_gmails > 0
    print(f"found {found_gmails} from gmails")

    found_gmails_raw = 0
    with open("fake_profiles.bson", "rb") as f:
        stream = BSONInput(fh=f, fast_string_prematch=b"@gmail.com", decode=False)
        for raw_bson in stream:
            assert b"@gmail" in raw_bson  # not even bothering to decode to a dict
            found_gmails_raw += 1
    assert found_gmails_raw > 0
    print(f"found {found_gmails_raw} from gmails without even decoding the BSON")