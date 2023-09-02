import React, { useEffect, useMemo, useState } from 'react'
import { Space, Select, Row, Col, Form, Avatar } from 'antd';
import { CodeSandboxOutlined } from '@ant-design/icons'

import { Function } from '../../../hooks/useFunctions'

type Props = {
    functions: Function[]
    initialFunctionVersionId?: string
    selectFunctionVersion?: (version?: string) => void
}

const SelectFunctionVersion = ({ selectFunctionVersion, functions, initialFunctionVersionId }: Props) => {

    const [functionId, setFunctionId] = useState<string>()

    const selectedFunction = useMemo(() => {
        return functions.find((func) => func.id === functionId)
    }, [functionId, functions])

    const versions = useMemo(() => {
        if (!selectedFunction) return []
        return selectedFunction.functionversionSet.edges.map((edge) => edge.node)
            .filter((node) => node.status === 'SUCCEEDED')
            .sort((a, b) => {
                if (a.createdAt > b.createdAt) return -1
                if (a.createdAt < b.createdAt) return 1
                return 0
            })
    }, [selectedFunction])

    const [version, setVersion] = useState<string | undefined>(initialFunctionVersionId)

    useEffect(() => {
        if (functions.length === 0) return
        if (initialFunctionVersionId === undefined) return setFunctionId(functions[0].id)

        const func = functions.find((func) => func.functionversionSet.edges.find((edge) => edge.node.id === initialFunctionVersionId))
        setFunctionId(func?.id)
    }, [functions, initialFunctionVersionId])

    useEffect(() => {
        if (versions.length === 0) return setVersion(undefined)
        if (initialFunctionVersionId) {
            const version = versions.find((v) => v.id === initialFunctionVersionId)
            if (version) return setVersion(version.id)
        }
        setVersion(versions[0].id)
    }, [selectedFunction, versions, initialFunctionVersionId])

    useEffect(() => {
        if (!selectFunctionVersion) return
        selectFunctionVersion(version)
    }, [version, selectFunctionVersion])



    return (
        <Row gutter={8}>
            <Col span={12}>
                <Select
                    value={functionId}
                    onChange={setFunctionId}
                    options={functions.map((func) => ({
                        label: (<Space>
                            <CodeSandboxOutlined />
                            <Avatar src={func.owner.avatar} size='small' />
                            {func.slug}
                        </Space>),
                        value: func.id
                    }))}
                />
            </Col>
            <Col span={12}>
                <Select
                    value={version}
                    onChange={setVersion}
                    options={versions.map((version) => ({
                        label: version.version,
                        value: version.id
                    }))}
                />
            </Col>
        </Row>

    )
}

export default SelectFunctionVersion