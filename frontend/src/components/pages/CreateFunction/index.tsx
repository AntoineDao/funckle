import React from 'react'
import { Button } from 'antd'
import CreateFunctionForm from '../../organisms/FunctionForm'
import Card from 'antd/es/card/Card'
import PageColumn from '../../templates/PageColumn'
import { Link } from 'react-router-dom'

const CreateFunction = () => {

    return (
        <PageColumn
            header={[
                <Link to="/functions">
                    <Button type="primary">
                        Back
                    </Button>
                </Link>
            ]}
        >

            <Card>
                <CreateFunctionForm />
            </Card>
        </PageColumn>

    )
}

export default CreateFunction