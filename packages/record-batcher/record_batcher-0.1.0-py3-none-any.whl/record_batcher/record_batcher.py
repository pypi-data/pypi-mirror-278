import random
import string
import sys

ONE_MEGABYTE = 1024 * 1024  # 1 MB


def generate_random_string(length: int) -> str:
    return "".join(
        random.choices(
            string.ascii_lowercase + string.ascii_uppercase + string.digits, k=length
        )
    )


class RecordBatcher:
    def __init__(
        self,
        max_record_size: int = ONE_MEGABYTE,
        max_batch_size: int = 5 * ONE_MEGABYTE,
        max_records_per_batch: int = 500,
        include_list_object_in_batch_size: bool = False,
        include_garbage_collector_overhead: bool = False,
    ):
        self.max_record_size = max_record_size
        self.max_batch_size = max_batch_size
        self.max_records_per_batch = max_records_per_batch
        self.include_list_object_in_batch_size = include_list_object_in_batch_size
        self.include_garbage_collector_overhead = include_garbage_collector_overhead

    def batch_records(self, records: list[str]) -> list[list[str]]:
        current_batch = []
        output_batches = []

        for record in records:
            if not isinstance(record, str):
                raise ValueError(f"Record must be a string, got {type(record)}")

            record_size = self._get_obj_size(record)

            if record_size > self.max_record_size:
                print(
                    f"Discarding record of size {record_size} due to exceeding "
                    f"the maximum record size of {self.max_record_size}"
                )
                continue

            if (
                self._get_batch_size(current_batch) + record_size > self.max_batch_size
                or len(current_batch) >= self.max_records_per_batch
            ):
                output_batches.append(current_batch)
                current_batch = []

            current_batch.append(record)

        # Add the last batch
        if current_batch:
            output_batches.append(current_batch)

        return output_batches

    def _get_obj_size(self, obj: str | list[str]):
        if self.include_garbage_collector_overhead:
            return sys.getsizeof(obj)
        return obj.__sizeof__()

    def _get_batch_size(self, batch: list[str]):
        if self.include_list_object_in_batch_size:
            return self._get_obj_size(batch) + sum(
                self._get_obj_size(record) for record in batch
            )
        return sum(self._get_obj_size(record) for record in batch)

    def generate_records(
        self,
        num_records: int = 1,
        record_sizes: list[int] | None = None,
        random_sizes: bool = False,
        record_size: int = ONE_MEGABYTE,
    ) -> list[str]:
        if not isinstance(num_records, int):
            raise ValueError(
                f"Number of records must be an integer, got {type(num_records)}"
            )

        base_string_size = self._get_obj_size("")
        record_size -= base_string_size

        if record_size < 0:
            raise ValueError(
                f"Record size must be greater than or equal to empty string size ({base_string_size} bytes)"
            )

        if isinstance(record_sizes, list):
            records = []
            for size in record_sizes:
                if not isinstance(size, int):
                    raise ValueError(
                        f"Record size must be an integer, got {type(size)}"
                    )

                if size < base_string_size:
                    raise ValueError(
                        f"Record size must be greater than or equal to empty string size ({base_string_size} bytes)"
                    )

                records.append(generate_random_string(size - base_string_size))

            return records

        if random_sizes:
            return [
                generate_random_string(random.randint(0, record_size))
                for _ in range(num_records)
            ]

        return [generate_random_string(record_size) for _ in range(num_records)]
