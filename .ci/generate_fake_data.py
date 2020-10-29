from faker import Faker
import bson
from bsonstream import BSONInput

fake = Faker()


# generate 5000 fake profiles, write them all into a bson object, then read back only those with @gmail.com emails


with open("fake_profiles.bson", "wb") as f:
    for _ in range(500):
        faked = fake.simple_profile()
        del faked['birthdate']  # bson doesn't like date wants datetime
        bson_data = bson.BSON.encode(faked)
        f.write(bson_data)

found_gmails = 0
with open("fake_profiles.bson", "rb") as f:
    stream = BSONInput(fh=f, fast_string_prematch=b"@gmail.com")
    for doc in stream:
        found_gmails += 1


assert found_gmails > 0
