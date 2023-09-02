import React from 'react'
import { Card, Badge, Row, Col, Typography, Space } from 'antd';
import Moment from 'react-moment';

import { FunctionVersion } from '../../../hooks/useFunction';

type Props = {
    version: string,
    status: string,
}

// PENDING
// STARTED
// RUNNING
// UNKNOWN
// SUCCEEDED
// FAILED

// use antd icons
const StatusIcon = ({ status }: FunctionVersion) => {
    switch (status) {
        case 'PENDING':
            return <Badge status="default" text="Pending" />
        case 'STARTED':
            return <Badge status="processing" text="Started" />
        case 'RUNNING':
            return <Badge status="processing" text="Running" />
        case 'UNKNOWN':
            return <Badge status="error" text="Unknown" />
        case 'SUCCEEDED':
            return <Badge status="success" text="Success" />
        case 'FAILED':
            return <Badge status="error" text="Error" />
        default:
            return <Badge status="default" text="Unknown" />
    }
}


const PackageMeta = (props: FunctionVersion) => {
    return (
        <Card.Meta
            title={props.version}
            description={
                <Row gutter={[8, 8]}>
                    <Col>
                        <StatusIcon {...props} />
                    </Col>
                    <Col>|</Col>
                    <Col>
                        <Typography.Text type="secondary">
                            Created
                        </Typography.Text>
                    </Col>
                    <Col>
                        <Moment fromNow>
                            {props.updatedAt}
                        </Moment>
                    </Col>
                    <Col>|</Col>
                    <Col>
                        <Typography.Text type="secondary">
                            Build Time
                        </Typography.Text>
                    </Col>
                    <Col>
                        <Moment
                            interval={1000}
                            durationFromNow={['SUCCEEDED', 'FAILED'].includes(props.status)}
                            duration={props.createdAt}
                            date={['SUCCEEDED', 'FAILED'].includes(props.status) ? props.updatedAt : undefined}
                        />

                    </Col>
                </Row>
            }
        />

    )
}

export default PackageMeta