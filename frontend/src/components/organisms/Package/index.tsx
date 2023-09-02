import React, { useMemo } from 'react'
import { useParams } from "react-router-dom";
import { Card, Col, Row, Typography } from 'antd';

import { useFunction } from '../../../hooks/useFunction';
import LogViewer from '../../atoms/LogViewer';
import PackageMeta from '../../molecules/PackageMeta';

type Props = {
    functionId: string
}

const Package = (props: Props) => {
    const { functionVersions } = useFunction({ id: props.functionId })
    let { versionId } = useParams();

    const functionVersion = useMemo(() => {
        return functionVersions.find((f) => f.id === versionId)
    }, [functionVersions, versionId])

    if (functionVersion === undefined) {
        return null
    }

    return (
        <Card>
            <Row gutter={[16, 16]}>
                <Col span={24}>
                    <PackageMeta {...functionVersion} />
                </Col>
                <Col span={24}>
                    <Typography.Title level={5}>Build Logs</Typography.Title>
                    <LogViewer logs={functionVersion.buildLogs.split('\n')} />
                </Col>
            </Row>
        </Card>

    )

}

export default Package