def main():
    filepath = "./keysight_chakra/protobuf/et_def.proto"
    original_package_name = "ChakraProtoMsg"
    new_package_name = "keysight_chakra.protobuf"
    with open(filepath, "r") as file:
        updated_text = file.read().replace(original_package_name, new_package_name)
    with open(filepath, "w") as file:
        file.write(updated_text)

if __name__ == "__main__":
    main()
