#ifndef _BYTEORDER_H_
#define _BYTEORDER_H_

#include <Python.h> /* required for WORDS_BIGENDIAN */

#ifndef WORDS_BIGENDIAN
  #define SWAB16(x) ((uint16_t)(                                  \
    (((uint16_t) (x) & (uint16_t) 0x00FFU) << 8) |                \
    (((uint16_t) (x) & (uint16_t) 0xFF00U) >> 8)))
  
  #define SWAB32(x) ((uint32_t)(                                  \
    (((uint32_t) (x) & (uint32_t) 0x000000FFUL) << 24) |          \
    (((uint32_t) (x) & (uint32_t) 0x0000FF00UL) <<  8) |          \
    (((uint32_t) (x) & (uint32_t) 0x00FF0000UL) >>  8) |          \
    (((uint32_t) (x) & (uint32_t) 0xFF000000UL) >> 24)))
  
  #define SWAB64(x) ((uint64_t)(                                  \
    (((uint64_t) (x) & (uint64_t) 0x00000000000000FFULL) << 56) | \
    (((uint64_t) (x) & (uint64_t) 0x000000000000FF00ULL) << 40) | \
    (((uint64_t) (x) & (uint64_t) 0x0000000000FF0000ULL) << 24) | \
    (((uint64_t) (x) & (uint64_t) 0x00000000FF000000ULL) <<  8) | \
    (((uint64_t) (x) & (uint64_t) 0x000000FF00000000ULL) >>  8) | \
    (((uint64_t) (x) & (uint64_t) 0x0000FF0000000000ULL) >> 24) | \
    (((uint64_t) (x) & (uint64_t) 0x00FF000000000000ULL) >> 40) | \
    (((uint64_t) (x) & (uint64_t) 0xFF00000000000000ULL) >> 56)))
#else
  #define SWAB16(x) (x)
  #define SWAB32(x) (x)
  #define SWAB64(x) (x)
#endif

#endif /* _BYTEORDER_H_ */

