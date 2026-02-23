#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

// Insecure string comparison (not constant time). Equivalent to memcmp. The time taken depends on the contents of the strings.
bool insecure_string_compare(const void *a, const void *b, size_t length)
{
    const char *ca = a, *cb = b;
    for (size_t i = 0; i < length; i++)
        if (ca[i] != cb[i])
            return false;
    return true;
}

// String comparison in constant time to prevent timing attacks. Equivalent to NetBSD's consttime_memequal() or OpenBSD's timingsafe_bcmp() and timingsafe_memcmp.
// Cf. https://en.wikipedia.org/wiki/Timing_attack
bool constant_time_string_compare_1(const void *a, const void *b, size_t length)
{
    const char *ca = a, *cb = b;
    bool result = true;
    for (size_t i = 0; i < length; i++)
        result &= ca[i] == cb[i];
    return result;
}

// Another implementation of constant time string comparison using XOR operation.
bool constant_time_string_compare_2(uint8_t *arr1, uint8_t *arr2, int len)
{
    uint8_t result = 0;
    for (int i = 0; i < len; i++)
    {
        result |= arr1[i] ^ arr2[i]; // XOR each byte and accumulate the result
    }
    return result == 0;
}
