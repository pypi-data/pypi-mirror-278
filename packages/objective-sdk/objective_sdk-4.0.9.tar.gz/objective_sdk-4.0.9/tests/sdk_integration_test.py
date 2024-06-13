def integration_test(api_key):
    from objective import Client

    client = Client(api_key=api_key)

    print("Clearing the object store")
    client.object_store.delete_objects(client.object_store.list_all_objects())

    objects = []
    print("Creating an object without an ID:")
    objects.append(
        {
            "title": "Sevendayz Men's Shady Records Eminem Hoodie Hoody Black Medium",
            "brand": "sevendayz",
            "imageURLHighRes": [
                "https://images-na.ssl-images-amazon.com/images/I/41gMYeiNASL.jpg"
            ],
        },
    )

    print("Upserting it...")
    client.object_store.upsert_objects(objects)

    print("Creating an object with an ID:")
    objects = []
    from objective import Object

    objects.append(
        Object(
            id="1",
            object={
                "title": "Sevendayz Men's Shady Records Eminem Hoodie Hoody Black Medium",
                "brand": "sevendayz",
                "imageURLHighRes": [
                    "https://images-na.ssl-images-amazon.com/images/I/41gMYeiNASL.jpg"
                ],
            },
        )
    )
    objects.append(
        {"id": "4", "object": {"x": 1}},
    )
    print("Upserting it...")
    client.object_store.upsert_objects(objects)

    print("Checking object store size:")
    print("Object store size:", client.object_store.size())
    assert client.object_store.size() == 3

    print("Checking that objects are correctly formated.")
    for object in client.object_store.get_all_objects():
        if object.id == "4":
            assert object.object["x"] == 1
        if object.id == "1":
            assert object.object["brand"] == "sevendayz"
        if object.id not in {"4", "1"}:
            assert object.object["brand"] == "sevendayz"

    print("Creating an index:")
    index = client.indexes.create_index(
        index_type="text-neural-base", fields={"searchable": ["title", "brand"]}
    )

    index.status(watch=True)

    print("Listing all indexes")
    assert len(client.indexes.list_indexes()) > 0

    print("Performing a search")
    assert len(index.search("test")["results"]) > 0

    print("Delete the index")
    index.delete()


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Plain API key.")
    parser.add_argument("api_key", type=str, help="API key for the application")

    args = parser.parse_args()
    api_key = args.api_key

    integration_test(api_key)


if __name__ == "__main__":
    main()
