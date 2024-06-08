/***************************************************//**
 * @file    STSAcquisitionDelayFeature.h
 * @date    November 2015
 * @author  Ocean Optics, Inc.
 *
 * This feature provides an interface to the acquisition
 * delay feature in the STS.
 *
 * LICENSE:
 *
 * SeaBreeze Copyright (C) 2015, Ocean Optics Inc
 *
 * Permission is hereby granted, free of charge, to any person obtaining
 * a copy of this software and associated documentation files (the
 * "Software"), to deal in the Software without restriction, including
 * without limitation the rights to use, copy, modify, merge, publish,
 * distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so, subject
 * to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included
 * in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 * IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
 * CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
 * TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 *******************************************************/

#ifndef STSACQUISITIONDELAYFEATURE_H
#define STSACQUISITIONDELAYFEATURE_H

#include "vendors/OceanOptics/features/acquisition_delay/AcquisitionDelayFeature.h"

namespace seabreeze {

    class STSAcquisitionDelayFeature : public AcquisitionDelayFeature {
    public:
        STSAcquisitionDelayFeature(std::vector<ProtocolHelper *> helpers);
        virtual ~STSAcquisitionDelayFeature();

        /* Inherited from AcquisitionDelayFeature */
        virtual unsigned long getAcquisitionDelayIncrementMicroseconds(
                    const Protocol &protocol, const Bus &bus);
        virtual unsigned long getAcquisitionDelayMaximumMicroseconds(
                    const Protocol &protocol, const Bus &bus);
        virtual unsigned long getAcquisitionDelayMinimumMicroseconds(
                    const Protocol &protocol, const Bus &bus);
    };

} /* end namespace seabreeze */

#endif /*  STSACQUISITIONDELAYFEATURE_H */
